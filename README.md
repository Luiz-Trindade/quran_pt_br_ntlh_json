# 🕌 Projeto de Tradução Acessível do Alcorão Sagrado

<p align="center">
  <img src="https://img.shields.io/badge/Open_Source-Yes-brightgreen.svg" alt="Open Source">
  <img src="https://img.shields.io/badge/Non--Profit-❤️-lightgrey.svg" alt="Non-Profit">
  <img src="https://img.shields.io/badge/AI_Powered-gemma3n:e4b-blue.svg" alt="AI Powered">
  <img src="https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/Language-PT--BR-green.svg" alt="Português">
</p>

## 🇧🇷 Português (pt-BR)

🌟 Este é um projeto **open-source e sem fins lucrativos** criado com o objetivo de tornar o Alcorão Sagrado mais acessível a todas as pessoas que desejam ter um primeiro contato com o texto, independentemente de serem ou não muçulmanas.

**Inspirado na NTLH** (Nova Tradução na Linguagem de Hoje), o projeto busca oferecer uma tradução para o português brasileiro em linguagem simples, natural, cotidiana e respeitosa, facilitando a compreensão para quem não fala árabe.

### ⚠️ Importante
**O Alcorão verdadeiro e autêntico é somente o revelado em árabe clássico.**  
Esta versão é uma **tradução dos significados** para o português, feita com o auxílio de inteligência artificial, com o único intuito de promover acessibilidade, estudo e curiosidade respeitosa. Não substitui o texto original em árabe.

### 📖 Como surgiu este projeto
Em nossas conversas anteriores, você buscava uma solução leve para rodar localmente no Linux usando **Ollama 100% em CPU** (sem drivers NVIDIA). Após testar vários modelos leves, escolhemos o **`gemma3n:e4b`** por ser um dos mais eficientes em tradução multilíngue, leve em memória e excelente em seguir regras e padrões de estilo (como o da NTLH).

O projeto utiliza esse modelo para traduzir do árabe para o português, mantendo fidelidade ao sentido original e adaptando para linguagem acessível.

### 🎯 Objetivo
Oferecer uma porta de entrada amigável para quem tem vontade ou curiosidade de conhecer o Alcorão de forma simples e pacífica.

---

## 🇬🇧 English (en)

🌟 This is an **open-source and non-profit project** created with the goal of making the Holy Quran more accessible to everyone who wishes to have a first contact with the text, whether they are Muslim or not.

**Inspired by NTLH** (Nova Tradução na Linguagem de Hoje – New Translation in Today's Language), the project aims to provide a translation into Brazilian Portuguese using simple, natural, everyday and respectful language, making it easier for those who do not speak Arabic.

### ⚠️ Important
**The true and authentic Quran is only the one revealed in classical Arabic.**  
This version is a **translation of the meanings** into Portuguese, created with the help of artificial intelligence, solely to promote accessibility, study and respectful curiosity. It does not replace the original Arabic text.

### 📖 How this project started
In our previous conversations, you were looking for a lightweight solution to run locally on Linux using **Ollama 100% on CPU** (without NVIDIA drivers). After testing several lightweight models, we chose **`gemma3n:e4b`** because it is one of the most efficient for multilingual translation, light on memory, and excellent at following rules and style guidelines (such as the NTLH style).

The project uses this model to translate from Arabic to Portuguese, maintaining fidelity to the original meaning and adapting it to accessible language.

### 🎯 Goal
To offer a friendly gateway for those who have the desire or curiosity to know the Quran in a simple and peaceful way.

---

## 🇸🇦 العربية (ar)

🌟 هذا مشروع **مفتوح المصدر وبدون أي أغراض ربحية**، أُنشئ بهدف جعل القرآن الكريم أكثر سهولة ووصولاً لكل من يرغب في التعرف على النص لأول مرة، سواء كان مسلماً أم لا.

**مستوحى من أسلوب NTLH** (الترجمة الجديدة بلغة اليوم)، يهدف المشروع إلى تقديم ترجمة إلى البرتغالية البرازيلية بلغة بسيطة، طبيعية، يومية واحترامية، لتسهيل الفهم على من لا يتحدثون العربية.

### ⚠️ مهم جداً
**القرآن الحقيقي والأصيل هو فقط ما أُنزل باللغة العربية الفصحى.**  
هذه النسخة هي **ترجمة للمعاني** إلى البرتغالية، تم إعدادها بمساعدة الذكاء الاصطناعي، بهدف وحيد هو تعزيز الوصولية والدراسة والفضول المحترم. **لا تحل محل النص الأصلي بالعربية.**

### 📖 كيف بدأ هذا المشروع
في محادثاتنا السابقة، كنت تبحث عن حل خفيف يعمل محلياً على لينكس باستخدام **Ollama 100% على المعالج (CPU)** بدون برامج تشغيل NVIDIA. بعد تجربة عدة نماذج خفيفة، اخترنا النموذج **`gemma3n:e4b`** لأنه من أكثر النماذج كفاءة في الترجمة متعددة اللغات، وخفيف على الذاكرة، وممتاز في اتباع القواعد والأنماط (مثل أسلوب NTLH).

يستخدم المشروع هذا النموذج لترجمة النصوص من العربية إلى البرتغالية مع الحفاظ على الوفاء للمعنى الأصلي وتكييفه بلغة سهلة الوصول.

### 🎯 الهدف
تقديم بوابة ودية لمن لديهم الرغبة أو الفضول في معرفة القرآن بطريقة بسيطة وسلمية.

---

## 🛠️ Como usar (Português)

1. Instale o Ollama (modo CPU only, conforme orientamos anteriormente).
2. Baixe o modelo:
   ```bash
   ollama run gemma3n:e4b# quran_pt_br_ntlh_json
