---
name: unity-docs-first
description: Mandatory documentation-first workflow for Unity. Before implementing any Unity feature, script, component, mechanic, or architecture, ALWAYS inspect the local official Unity 6 documentation at C:\Program Files\Unity\Hub\Editor\6000.6.2f1\Editor\Data\Documentation\en\, analyze the exact API signatures, component lifecycles, and replicate official Unity best practices.
---

# Unity Docs-First Skill (Obrigatório / Mandatory)

Esta skill estabelece a **obrigatoriedade** de consultar e analisar a documentação oficial da Unity antes de planejar, escrever ou modificar qualquer código, script C#, componente ou sistema de jogo.

---

## 📚 Localização da Documentação Oficial Instalada (Local)

A documentação completa e offline do **Unity 6 (6000.6.2f1)** está localizada no disco local:
- **Diretório Base**: `C:\Program Files\Unity\Hub\Editor\6000.6.2f1\Editor\Data\Documentation\en\`
- **Script Reference (APIs, Classes, Métodos)**: `C:\Program Files\Unity\Hub\Editor\6000.6.2f1\Editor\Data\Documentation\en\ScriptReference\`
- **Manual Oficial (Conceitos, Guias, Workflows)**: `C:\Program Files\Unity\Hub\Editor\6000.6.2f1\Editor\Data\Documentation\en\Manual\`

---

## ⚡ Protocolo Obrigatório em 4 Etapas

Sempre que o usuário solicitar a criação, alteração ou depuração de qualquer funcionalidade na Unity:

### 1. Pesquisa e Leitura Prévia da Documentação (OBRIGATÓRIO)
Antes de criar ou editar qualquer arquivo:
- Verifique se a classe ou método existe na documentação local:
  Exemplo:
  - `ScriptReference/MonoBehaviour.html`
  - `ScriptReference/Rigidbody2D.html`
  - `ScriptReference/CharacterController.html`
  - `ScriptReference/Animator.html`
  - `ScriptReference/Input.html`
- Para buscar rapidamente via PowerShell:
  ```powershell
  powershell -ExecutionPolicy Bypass -File "C:\Users\alexa\.gemini\config\skills\unity-docs-first\scripts\search-unity-docs.ps1" -Query "<NomeDaClasse>"
  ```

### 2. Análise Técnica dos Métodos e Assinaturas
- Analise os parâmetros, tipos de retorno e ciclo de vida (`Awake` -> `OnEnable` -> `Start` -> `FixedUpdate` -> `Update` -> `LateUpdate` -> `OnDisable` -> `OnDestroy`).
- **Atenção às mudanças de versão do Unity 6**:
  - Exemplo: Uso de `rb.linearVelocity` em vez do obsoleto `rb.velocity`.
  - Checar convenções modernas de eventos e atributos (`[SerializeField]`, `[RequireComponent]`, `[Range]`, etc.).

### 3. Replicação Fiel ao Padrão da Unity
- Implemente a solução seguindo rigorosamente a assinatura e os exemplos de código da documentação oficial.
- Evite suposições ou APIs obsoletas.

### 4. Validação e Console
- Imediatamente após a compilação no Editor, execute `Unity_ReadConsole` para garantir que não há erros ou advertências de depreciação.

---

## 🛠️ Exemplos de Páginas de Referência Frequentes

| Tópico | Caminho do Arquivo Local |
| :--- | :--- |
| **Ciclo de Vida de Scripts** | `.../Manual/execution-order.html` |
| **MonoBehaviour Base** | `.../ScriptReference/MonoBehaviour.html` |
| **Física 2D (Rigidbody2D)** | `.../ScriptReference/Rigidbody2D.html` |
| **Colisores 2D (Collider2D)** | `.../ScriptReference/Collider2D.html` |
| **Animações (Animator)** | `.../ScriptReference/Animator.html` |
| **Câmera 2D/3D** | `.../ScriptReference/Camera.html` |
| **Input System** | `.../Manual/com.unity.inputsystem.html` |
