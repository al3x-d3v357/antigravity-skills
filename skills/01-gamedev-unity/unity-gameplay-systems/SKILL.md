---
name: unity-gameplay-systems
description: Architecture, best practices, and automation for Unity gameplay development, C# scripts, Player Controllers (2D/3D), Cinemachine/cameras, Game Managers, health/combat systems, UI Canvas (TMP), and audio triggers via Unity-MCP. Use whenever creating or debugging game mechanics, player movement, physics, game loop logic, or interactive gameplay elements in Unity.
---

# Unity Gameplay Systems & Architecture Guide

This skill provides patterns, reusable C# architecture, and MCP workflows for building gameplay systems in Unity.

---

## ⚡ Critical Unity-MCP Compilation Rule

Whenever creating or updating scripts via MCP tools:
1. Use `create_script` or `script_apply_edits`.
2. Both tools automatically trigger `AssetDatabase.ImportAsset` and compilation.
3. **Always poll/wait** for `is_compiling == false` via `mcpforunity://editor/state`.
4. **Always check `read_console`** immediately:
   ```json
   {"types": ["error"], "count": 10, "include_stacktrace": true}
   ```
5. Do NOT attach a script to a GameObject before compilation finishes without errors.

---

## 🎮 1. Player Controller Patterns

### CharacterController (Recommended for responsive 3D Platformers / Action)
- Uses `CharacterController.Move()`.
- Calculates gravity manually (`velocity.y += Physics.gravity.y * Time.deltaTime`).
- Smooth rotation towards movement direction (`Quaternion.Slerp` / `Mathf.Atan2`).
- Ground check via `CharacterController.isGrounded` or a sphere cast at feet.

### Rigidbody Controller (Recommended for Physics-driven / Vehicle / Ragdoll games)
- Movement applied in `FixedUpdate` using `rb.MovePosition`, `rb.AddForce`, or modifying `rb.linearVelocity`.
- Always set `Interpolate` to `Interpolate` on the Rigidbody for smooth camera tracking.
- Freeze rotation constraints on X and Z for upright characters.

---

## 🕹️ 2. Modern Input System (`UnityEngine.InputSystem`)

Prefer the new Input System:
```csharp
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif
```
- For quick prototyping: `Keyboard.current.wKey.isPressed` or `Gamepad.current.leftStick.ReadValue()`.
- For production: Use PlayerInput component or generated C# class from `.inputactions`.

---

## 🏛️ 3. Core Architecture & Game Loop

### GameManager (Persistent Singleton pattern)
```csharp
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Game State")]
    public int currentScore = 0;
    public bool isGameOver = false;

    private void Awake()
    {
        if (Instance != null && Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void AddScore(int amount)
    {
        currentScore += amount;
        // Invoke UI update events
    }
}
```

### Health & Damage System (`IDamageable`)
- Define an interface `IDamageable` with `void TakeDamage(float amount, Vector3 hitPoint)`.
- Player, enemies, and destructible objects implement `IDamageable`.
- Allows weapons and projectiles to damage anything without tight coupling (`if (hit.TryGetComponent<IDamageable>(out var target)) target.TakeDamage(...)`).

---

## 🖥️ 4. UI Canvas & TextMeshPro (TMP)

- Use TextMeshPro (`TMPro.TextMeshProUGUI`) instead of legacy `UnityEngine.UI.Text`.
- Anchor presets:
  - Health bar: Top-Left
  - Score / Coins: Top-Right
  - Crosshair: Center
  - Dialogue / Subtitles: Bottom-Center
- Use `CanvasScaler` configured to `Scale With Screen Size` (Reference Resolution `1920x1080`, Match `0.5`).

---

## 🔊 5. Audio & Feedback

- Create an `AudioManager` or place `AudioSource` on audio triggers.
- For 3D spatial sounds: Set `spatialBlend` to `1.0` and configure min/max distance roll-off.
- For 2D UI / BG Music: Set `spatialBlend` to `0.0`.
- Play one-shot sound effects without allocating new objects: `audioSource.PlayOneShot(clip)`.

---

## 📋 Checklist for New Game Features

1. [ ] Script structure defined with clean fields (`[SerializeField] private float moveSpeed = 6f;`).
2. [ ] Headers & tooltips added for Unity Inspector clarity (`[Header("Settings")]`).
3. [ ] Script created and compiled without errors in Unity Console.
4. [ ] GameObject created or found in scene hierarchy.
5. [ ] Script component attached via `manage_components(action="add", ...)`.
6. [ ] Required references wired up in Inspector or via `GetComponent<T>()` in `Awake()`.
