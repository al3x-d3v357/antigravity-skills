---
name: toycub-blender-animator
description: Automação completa de animações procedurais e estilizadas para personagens do estilo ToyCube (rig vertical de 3 ossos: Base, Tronco e Cabeça). Gera pacote com 8 Actions completas (4 principais + 4 extras com +70% de conteúdo: Walk_Hop, Attack_TopBone, Skill_Cast com suporte a VFX/Laser, Death_Backflip, Idle_Breathing, Hit_React, Spawn_Drop e Victory_Spin) compatível com Blender e exportação GLB para Godot.
---

# ToyCube Blender Animator (8 Actions Suite)

Skill especializada na geração automática e procedural de animações estilizadas para personagens da linhagem **ToyCube** no Blender (como o `cyclop.blend`), projetada para rigs com cadeia vertical de 3 ossos (`root`/`Osso_Base`, `mid`/`Osso_Tronco`, `top`/`Osso_Cabeca`), com suporte modular a membros (`Hand.L`, `Hand.R`) e malhas de efeito vinculadas (ex: objeto `laser`).

---

## 📦 Pacote de 8 Animações de Jogo

| Action | Tipo | Frames | Curva / Estilo Visual |
| :--- | :--- | :--- | :--- |
| **`Walk_Hop`** | Principal | `0 - 16` | Salto elástico com antecipação (Squash no f4), ápice com inclinação frontal (Stretch no f8) e amortecimento elástico no solo (f12). |
| **`Attack_TopBone`** | Principal | `0 - 16` | Ataque mecânico exclusivo do 3º osso superior: recuo/carregamento elástico (f5) seguido de chicotada violenta para frente (f8) e overshoot elástico (f11). |
| **`Skill_Cast`** | Condicional | `0 - 28` | Carga energética inclinando o topo e tronco para trás com trepidação (f0-10) e disparo contínuo frontal (f12-20), animando em conjunto a escala do mesh `laser`. |
| **`Death_Backflip`** | Principal | `0 - 24` | Tranco fatal com pulo recuado (f4-10) e rotação de 90° de costas caindo deitado (f16), finalizando com quique elástico (f19-24). |
| **`Idle_Breathing`** | Extra (+70%) | `0 - 40` | Ciclo orgânico de respiração em loop infinito com micro-escala e leve oscilação no topo. |
| **`Hit_React`** | Extra (+70%) | `0 - 12` | Recuo instantâneo dos ossos médios e superiores simulando absorção de impacto físico/projétil. |
| **`Spawn_Drop`** | Extra (+70%) | `0 - 20` | Entrada em cena caindo do ar esticado, comprimindo contra o solo no impacto (f8) e estabilizando. |
| **`Victory_Spin`** | Extra (+70%) | `0 - 24` | Salto de vitória com rotação longitudinal completa de 360° no ar e pouso comemorativo. |

---

## ⚙️ Parâmetros Modulares de Configuração

Ao acionar a skill para um novo modelo ToyCube, defina os parâmetros no cabeçalho do script:

- `ARMATURE_NAME`: Nome do objeto Armature na cena (padrão: `"Armature"`).
- `EFFECT_MESH_NAME`: Nome da malha de efeito visual atrelada ao disparo (ex: `"laser"`). Se existir, recebe a action sincronizada `Skill_Laser_VFX`.
- `HAS_SKILL`: `True` para personagens conjuradores/atiradores; `False` para unidades corpo a corpo básicas.
- `HAS_HANDS`: `True` para animar ossos de mão/braço (`Hand.L`, `Hand.R`, `Arm.L`, `Arm.R`).
- `PITCH_AXIS`: `0` para rotação frontal no eixo X local (padrão Blender).

---

## 🐍 Script de Automação Blender (`bpy`)

```python
import bpy
import math

# ==============================================================================
# CONFIGURAÇÕES MODULARES DO PERSONAGEM (TOYCUBE RIG)
# ==============================================================================
ARMATURE_NAME = "Armature"
EFFECT_MESH_NAME = "laser"  # Objeto de efeito na cena (ex: laser do Cyclop)

HAS_SKILL = True            # True = Gera Skill_Cast | False = Pula criação de habilidade
HAS_HANDS = False           # True = Anima ossos Hand.L / Hand.R se existirem

# Eixo de inclinação frontal (Pitch) dos ossos no modo Pose:
# 0 = Eixo X local (Padrão Blender) | 2 = Eixo Z local
PITCH_AXIS = 0
YAW_AXIS = 1                # Eixo longitudinal do osso (rotação lateral/giro)
ROLL_AXIS = 2


def get_armature_and_bones(arm_name):
    arm_obj = bpy.data.objects.get(arm_name)
    if not arm_obj or arm_obj.type != 'ARMATURE':
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                arm_obj = obj
                break
    if not arm_obj:
        raise RuntimeError(f"Nenhuma Armature encontrada na cena (esperado: '{arm_name}').")

    bpy.context.view_layer.objects.active = arm_obj
    if arm_obj.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')

    # Ordena a cadeia principal de 3 ossos pela hierarquia (de baixo para cima)
    roots = [b for b in arm_obj.pose.bones if b.parent is None]
    if not roots:
        raise RuntimeError("Armature não possui osso raiz.")

    root_bone = roots[0]
    mid_bone = root_bone.children[0] if root_bone.children else None
    top_bone = mid_bone.children[0] if (mid_bone and mid_bone.children) else None

    if not (root_bone and mid_bone and top_bone):
        all_bones = list(arm_obj.pose.bones)
        if len(all_bones) >= 3:
            root_bone, mid_bone, top_bone = all_bones[0], all_bones[1], all_bones[2]
        else:
            raise RuntimeError("A Armature precisa ter pelo menos 3 ossos para o ToyCube.")

    # Mapeamento opcional de mãos/braços
    hand_l = arm_obj.pose.bones.get("Hand.L") or arm_obj.pose.bones.get("Arm.L")
    hand_r = arm_obj.pose.bones.get("Hand.R") or arm_obj.pose.bones.get("Arm.R")

    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'

    return arm_obj, root_bone, mid_bone, top_bone, hand_l, hand_r


def reset_pose(arm_obj):
    for pb in arm_obj.pose.bones:
        pb.location = (0.0, 0.0, 0.0)
        pb.rotation_euler = (0.0, 0.0, 0.0)
        pb.scale = (1.0, 1.0, 1.0)


def create_new_action(arm_obj, action_name):
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    
    old_act = bpy.data.actions.get(action_name)
    if old_act:
        bpy.data.actions.remove(old_act)

    action = bpy.data.actions.new(name=action_name)
    action.use_fake_user = True
    arm_obj.animation_data.action = action
    reset_pose(arm_obj)
    return action


def key_bone(pbone, frame, loc=None, rot_deg=None, scale=None):
    if loc is not None:
        pbone.location = loc
        pbone.keyframe_insert(data_path="location", frame=frame)
    if rot_deg is not None:
        pbone.rotation_euler = tuple(math.radians(a) for a in rot_deg)
        pbone.keyframe_insert(data_path="rotation_euler", frame=frame)
    if scale is not None:
        pbone.scale = scale
        pbone.keyframe_insert(data_path="scale", frame=frame)


def make_rot(pitch=0.0, yaw=0.0, roll=0.0):
    rot = [0.0, 0.0, 0.0]
    rot[PITCH_AXIS] = pitch
    rot[YAW_AXIS] = yaw
    rot[ROLL_AXIS] = roll
    return tuple(rot)


def smooth_action_curves(action):
    fcurves = getattr(action, "fcurves", None)
    if fcurves:
        for fc in fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'


def build_toycub_animations():
    arm_obj, root, mid, top, hand_l, hand_r = get_armature_and_bones(ARMATURE_NAME)
    laser_obj = bpy.data.objects.get(EFFECT_MESH_NAME)

    created_actions = []

    # 1. IDLE_BREATHING (0 a 40)
    act = create_new_action(arm_obj, "Idle_Breathing")
    for f in (0, 40):
        key_bone(root, f, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(mid, f, rot_deg=make_rot(0, 0, 0), scale=(1.0, 1.0, 1.0))
        key_bone(top, f, rot_deg=make_rot(0, 0, 0), scale=(1.0, 1.0, 1.0))
    key_bone(mid, 20, rot_deg=make_rot(-2, 0, 0), scale=(1.03, 0.96, 1.03))
    key_bone(top, 20, rot_deg=make_rot(4, 3, 0), scale=(1.02, 1.02, 1.02))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 40))

    # 2. WALK_HOP (0 a 16)
    act = create_new_action(arm_obj, "Walk_Hop")
    for f in (0, 16):
        key_bone(root, f, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(mid, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(top, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(root, 4, loc=(0, -0.02, 0), rot_deg=make_rot(5, 0, 0), scale=(1.08, 0.85, 1.08))
    key_bone(mid, 4, rot_deg=make_rot(8, 0, 0), scale=(1.1, 0.85, 1.1))
    key_bone(top, 4, rot_deg=make_rot(-6, 0, 0))
    key_bone(root, 8, loc=(0, 0.35, 0), rot_deg=make_rot(12, 0, 0), scale=(0.94, 1.12, 0.94))
    key_bone(mid, 8, rot_deg=make_rot(-5, 0, 0), scale=(0.95, 1.1, 0.95))
    key_bone(top, 8, rot_deg=make_rot(10, 0, 0))
    key_bone(root, 12, loc=(0, 0.0, 0), rot_deg=make_rot(-6, 0, 0), scale=(1.12, 0.82, 1.12))
    key_bone(mid, 12, rot_deg=make_rot(10, 0, 0), scale=(1.08, 0.88, 1.08))
    key_bone(top, 12, rot_deg=make_rot(14, 0, 0))
    if HAS_HANDS and hand_l and hand_r:
        for f in (0, 16):
            key_bone(hand_l, f, rot_deg=make_rot(0, 0, 0))
            key_bone(hand_r, f, rot_deg=make_rot(0, 0, 0))
        key_bone(hand_l, 8, rot_deg=make_rot(-35, 0, -15))
        key_bone(hand_r, 8, rot_deg=make_rot(-35, 0, 15))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 16))

    # 3. ATTACK_TOPBONE (0 a 16)
    act = create_new_action(arm_obj, "Attack_TopBone")
    for f in (0, 16):
        key_bone(root, f, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(mid, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(top, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 5, rot_deg=make_rot(-28, 0, 0), scale=(0.95, 1.08, 0.95))
    key_bone(top, 8, rot_deg=make_rot(45, 0, 0), scale=(1.1, 0.92, 1.15))
    key_bone(top, 11, rot_deg=make_rot(-8, 0, 0), scale=(1.0, 1.0, 1.0))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 16))

    # 4. SKILL_CAST (0 a 28)
    if HAS_SKILL:
        act = create_new_action(arm_obj, "Skill_Cast")
        for f in (0, 28):
            key_bone(root, f, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
            key_bone(mid, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
            key_bone(top, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(mid, 6, rot_deg=make_rot(-12, 0, 0), scale=(1.12, 0.88, 1.12))
        key_bone(top, 6, rot_deg=make_rot(-25, 4, 0), scale=(1.1, 0.9, 1.1))
        key_bone(top, 8, rot_deg=make_rot(-28, -4, 0), scale=(1.15, 0.85, 1.15))
        key_bone(top, 10, rot_deg=make_rot(-30, 0, 0), scale=(1.18, 0.82, 1.18))
        key_bone(root, 12, loc=(0, 0, 0), rot_deg=make_rot(-5, 0, 0))
        key_bone(mid, 12, rot_deg=make_rot(15, 0, 0), scale=(0.95, 1.08, 0.95))
        key_bone(top, 12, rot_deg=make_rot(35, 0, 0), scale=(1.08, 1.0, 1.15))
        key_bone(top, 20, rot_deg=make_rot(32, 0, 0), scale=(1.05, 1.0, 1.1))

        if laser_obj:
            if not laser_obj.animation_data:
                laser_obj.animation_data_create()
            laser_act = bpy.data.actions.get("Skill_Laser_VFX")
            if laser_act:
                bpy.data.actions.remove(laser_act)
            laser_act = bpy.data.actions.new(name="Skill_Laser_VFX")
            laser_act.use_fake_user = True
            laser_obj.animation_data.action = laser_act

            for f, sc in [(0, (0.01, 0.01, 0.01)), (10, (0.01, 0.01, 0.01)),
                          (12, (1.2, 2.5, 1.2)), (20, (1.0, 2.2, 1.0)), (24, (0.01, 0.01, 0.01))]:
                laser_obj.scale = sc
                laser_obj.keyframe_insert(data_path="scale", frame=f)

        smooth_action_curves(act)
        created_actions.append((act.name, 0, 28))

    # 5. DEATH_BACKFLIP (0 a 24)
    act = create_new_action(arm_obj, "Death_Backflip")
    key_bone(root, 0, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(mid, 0, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 0, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(root, 4, loc=(0, 0.05, -0.05), rot_deg=make_rot(-15, 0, 0), scale=(1.1, 0.88, 1.1))
    key_bone(mid, 4, rot_deg=make_rot(-15, 0, 0))
    key_bone(top, 4, rot_deg=make_rot(-25, 0, 0))
    key_bone(root, 10, loc=(0, 0.45, -0.35), rot_deg=make_rot(-50, 0, 0), scale=(0.95, 1.08, 0.95))
    key_bone(mid, 10, rot_deg=make_rot(-10, 0, 0))
    key_bone(top, 10, rot_deg=make_rot(-15, 0, 0))
    key_bone(root, 16, loc=(0, 0.15, -0.65), rot_deg=make_rot(-90, 0, 0), scale=(1.15, 0.85, 1.15))
    key_bone(mid, 16, rot_deg=make_rot(8, 0, 0))
    key_bone(top, 16, rot_deg=make_rot(12, 0, 0))
    key_bone(root, 19, loc=(0, 0.22, -0.70), rot_deg=make_rot(-86, 0, 0), scale=(1.0, 1.0, 1.0))
    key_bone(root, 24, loc=(0, 0.15, -0.72), rot_deg=make_rot(-90, 0, 0), scale=(1, 1, 1))
    key_bone(mid, 24, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 24, rot_deg=make_rot(-5, 0, 0), scale=(1, 1, 1))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 24))

    # 6. HIT_REACT (0 a 12)
    act = create_new_action(arm_obj, "Hit_React")
    for f in (0, 12):
        key_bone(root, f, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(mid, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
        key_bone(top, f, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(root, 3, loc=(0, 0, -0.08), rot_deg=make_rot(-8, 0, 0), scale=(1.12, 0.85, 1.12))
    key_bone(mid, 3, rot_deg=make_rot(-18, 0, 0))
    key_bone(top, 3, rot_deg=make_rot(-30, 8, 0))
    key_bone(top, 7, rot_deg=make_rot(10, -4, 0))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 12))

    # 7. SPAWN_DROP (0 a 20)
    act = create_new_action(arm_obj, "Spawn_Drop")
    key_bone(root, 0, loc=(0, 1.5, 0), rot_deg=make_rot(0, 0, 0), scale=(0.85, 1.25, 0.85))
    key_bone(mid, 0, rot_deg=make_rot(0, 0, 0), scale=(0.9, 1.15, 0.9))
    key_bone(top, 0, rot_deg=make_rot(-10, 0, 0), scale=(1, 1, 1))
    key_bone(root, 8, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1.25, 0.68, 1.25))
    key_bone(mid, 8, rot_deg=make_rot(10, 0, 0), scale=(1.2, 0.75, 1.2))
    key_bone(top, 8, rot_deg=make_rot(18, 0, 0), scale=(1.15, 0.85, 1.15))
    key_bone(root, 13, loc=(0, 0.12, 0), rot_deg=make_rot(0, 0, 0), scale=(0.94, 1.1, 0.94))
    key_bone(mid, 13, rot_deg=make_rot(-5, 0, 0), scale=(0.95, 1.08, 0.95))
    key_bone(top, 13, rot_deg=make_rot(-8, 0, 0), scale=(1, 1, 1))
    key_bone(root, 20, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(mid, 20, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 20, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 20))

    # 8. VICTORY_SPIN (0 a 24)
    act = create_new_action(arm_obj, "Victory_Spin")
    key_bone(root, 0, loc=(0, 0, 0), rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(mid, 0, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 0, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(root, 4, loc=(0, 0, 0), rot_deg=make_rot(0, -30, 0), scale=(1.12, 0.82, 1.12))
    key_bone(root, 12, loc=(0, 0.5, 0), rot_deg=make_rot(-8, 180, 0), scale=(0.92, 1.12, 0.92))
    key_bone(top, 12, rot_deg=make_rot(-15, 0, 0))
    key_bone(root, 18, loc=(0, 0, 0), rot_deg=make_rot(6, 360, 0), scale=(1.1, 0.86, 1.1))
    key_bone(root, 24, loc=(0, 0, 0), rot_deg=make_rot(0, 360, 0), scale=(1, 1, 1))
    key_bone(mid, 24, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    key_bone(top, 24, rot_deg=make_rot(0, 0, 0), scale=(1, 1, 1))
    smooth_action_curves(act)
    created_actions.append((act.name, 0, 24))

    # Padrão ativo: Walk_Hop
    arm_obj.animation_data.action = bpy.data.actions.get("Walk_Hop")
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 16
    bpy.context.scene.frame_set(0)

    print("=== PACOTE TOYCUB GERADO COM SUCESSO ===")
    for name, start, end in created_actions:
        print(f" -> Action: {name} (Frames {start} a {end})")

build_toycub_animations()
```

---

## 🎯 Integração Godot Engine 4 (GLB Pipeline)

1. **Exportação no Blender**:
   - `File` > `Export` > `glTF 2.0 (.glb)`.
   - Na aba **Animation**:
     - Ative **Animation** e **Group by NLA Track** ou assegure que todas as ações tenham `Fake User` (`use_fake_user = True`, já feito pelo script).
2. **Importação na Godot**:
   - As 8 Actions são importadas no nó `AnimationPlayer` como clips separados prontos para máquina de estados `AnimationTree` (`StateMachine`).
