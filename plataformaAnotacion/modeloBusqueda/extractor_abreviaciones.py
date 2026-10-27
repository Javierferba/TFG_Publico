import json
import re
import torch

class ExtractorAbreviaciones:
    def __init__(self, ruta_modelo, ruta_prompt):
        self.model_path = ruta_modelo
        self.prompt = self._cargar_prompt(ruta_prompt)

    def _cargar_prompt(self, ruta_prompt):
        with open(ruta_prompt, "r", encoding="utf-8") as file:
            return file.read()
    
    def _extraer_listas(self, texto):
        patrones = {
            "formas_abreviadas": re.compile(r'"formas_abreviadas": \[([^\]]+)\]'),
            "simbolos_medicos": re.compile(r'"simbolos_medicos": \[([^\]]+)\]')
        }
        datos = {"formas_abreviadas": [], "simbolos_medicos": []}
        for clave, patron in patrones.items():
            coincidencia = patron.search(texto)
            if coincidencia:
                elementos = [x.strip().strip('"') for x in coincidencia.group(1).split(',')]
                datos[clave] = elementos
        
        return datos

    def extraer_abreviaciones(self, model, tokenizer, texto, device="cpu"):
        datos = self.extraer_abreviaciones_simbolos(model, tokenizer, texto, device)
        return list(set(datos["formas_abreviadas"]) | set(datos["simbolos_medicos"]))
 
    def extraer_abreviaciones_simbolos(self, model, tokenizer, text, device="cpu", temperature=0.0, max_new_tokens=128):
        """
        Extrae abreviaciones y símbolos médicos de un texto usando transformers.
        
        Args:
            model: Modelo de transformers cargado
            tokenizer: Tokenizer correspondiente al modelo
            text (str): El texto a analizar
            device (str): Dispositivo donde ejecutar el modelo ('cpu' o 'cuda')
            temperature (float): Valor de temperatura para la generación
            max_new_tokens (int): Número máximo de tokens a generar
            
        Returns:
            dict: Diccionario con las listas de formas abreviadas y símbolos médicos
        """
        
        try:
            # Preparar el prompt completo
            messages = [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": text}
            ]
            
            # Formatear el prompt según el formato del modelo
            # Si el modelo tiene chat template, usarlo
            if hasattr(tokenizer, 'apply_chat_template'):
                prompt_formatted = tokenizer.apply_chat_template(
                    messages, 
                    tokenize=False, 
                    add_generation_prompt=True
                )
            else:
                # Formato alternativo si no tiene chat template
                prompt_formatted = f"{self.prompt}\n\nTexto: {text}\n\nRespuesta:"
            
            # Tokenizar
            inputs = tokenizer(prompt_formatted, return_tensors="pt").to(device)
            
            # Generar respuesta
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature if temperature > 0 else 1.0,
                    do_sample=temperature > 0,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decodificar la respuesta
            resp = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            
            # Intentar parsear como JSON
            try:
                resultado = json.loads(resp)
                return resultado
            except json.JSONDecodeError:
                inicio_json = resp.find("{")
                if inicio_json != -1:
                    json_str = resp[inicio_json:]
                    try:
                        resultado = json.loads(json_str)
                        return resultado
                    except json.JSONDecodeError:
                        listas = self._extraer_listas(resp)
                        return listas
                else:
                    return self._extraer_listas(resp)
                    
        except Exception as e:
            print(f"Error en la generación: {str(e)}")
            return {"formas_abreviadas": [], "simbolos_medicos": []}