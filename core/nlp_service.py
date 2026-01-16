import os
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Configura a API com a chave secreta
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ler_arquivo(caminho_arquivo):
    """Extrai texto cru de arquivos PDF ou TXT"""
    ext = os.path.splitext(caminho_arquivo)[1].lower()
    texto_completo = ""

    if ext == '.txt':
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            texto_completo = f.read()
    
    elif ext == '.pdf':
        try:
            reader = pypdf.PdfReader(caminho_arquivo)
            for page in reader.pages:
                texto_completo += page.extract_text() + "\n"
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return ""

    return texto_completo

def analisar_email_com_gemini(texto_email):
    """
    Envia o texto para o Gemini e pede uma análise estruturada.
    """
    if not api_key:
        return {
            "categoria": "Erro",
            "motivo": "Chave de API não configurada.",
            "sugestao_resposta": "Verifique o arquivo da chave API"
        }

    # Modelo mais rápido e barato para tarefas de texto
    model = genai.GenerativeModel('gemini-2.5-flash')

    # O Prompt é a "ordem" que damos para a IA
    prompt = f"""
    Aja como um assistente de suporte técnico. Analise o seguinte email:
    
    --- INÍCIO DO EMAIL ---
    {texto_email}
    --- FIM DO EMAIL ---

    Sua tarefa:
    1. Classifique se é "Produtivo" (precisa de ação/resposta técnica) ou "Improdutivo" (agradecimentos/felicitacoes).
    2. Explique brevemente o motivo.
    3. Se for Produtivo, escreva uma sugestão de resposta educada e profissional. Se for Improdutivo, a sugestão deve ser uma mensagem retribuindo o agradecimento.

    Responda EXATAMENTE neste formato padrão (sem markdown de código):
    Categoria: [Produtivo/Improdutivo]
    Motivo: [Sua explicação curta]
    Resposta Sugerida: [O texto da resposta]
    """

    try:
        response = model.generate_content(prompt)
        texto_resposta = response.text
        
        # Vamos fazer um "parse" simples para separar os campos
        linhas = texto_resposta.split('\n')
        resultado = {
            "categoria": "Indefinido",
            "motivo": "",
            "sugestao_resposta": ""
        }
        
        buffer_resposta = False
        resposta_acumulada = []

        for linha in linhas:
            if linha.startswith("Categoria:"):
                resultado["categoria"] = linha.replace("Categoria:", "").strip()
            elif linha.startswith("Motivo:"):
                resultado["motivo"] = linha.replace("Motivo:", "").strip()
            elif linha.startswith("Resposta Sugerida:"):
                buffer_resposta = True
                texto = linha.replace("Resposta Sugerida:", "").strip()
                if texto: resposta_acumulada.append(texto)
            elif buffer_resposta:
                resposta_acumulada.append(linha)
        
        resultado["sugestao_resposta"] = "\n".join(resposta_acumulada).strip()
        
        return resultado

    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        return {
            "categoria": "Erro na IA",
            "motivo": "Não foi possível conectar ao Gemini.",
            "sugestao_resposta": "Tente novamente mais tarde."
        }