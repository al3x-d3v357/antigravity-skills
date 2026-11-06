#!/usr/bin/env python3
"""
Pipeline de Execução em Segundo Plano:
Envio Real de Candidaturas (Auto-Apply)
- 300 Vagas Home Office / Remoto
- 300 Vagas PcD (Pessoa com Deficiência)
"""

import os
import sys
import json
import time
import asyncio
import logging
from pathlib import Path
from browser_engine import JobBrowserEngine
from tracker import ApplicationsTracker, load_config

SCRIPTS_DIR = Path(__file__).resolve().parent
LOG_FILE = SCRIPTS_DIR / "auto_apply_300.log"
STATUS_FILE = SCRIPTS_DIR / "auto_apply_status.json"

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def update_status(data: dict):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.warning(f"Erro ao atualizar status: {e}")

async def process_target_category(
    category_name: str,
    target_count: int,
    engine: JobBrowserEngine,
    tracker: ApplicationsTracker,
    is_home_office: bool = False,
    is_pcd: bool = False,
    overall_progress: dict = None
):
    logging.info("=" * 70)
    logging.info(f" [INÍCIO CATEGORIA] {category_name.upper()} - META: {target_count} CANDIDATURAS")
    logging.info("=" * 70)

    # 1. Mapeamento das vagas
    logging.info(f">> Coletando vagas disponíveis para {category_name} no InfoJobs...")
    collected_jobs = await engine.search_infojobs_jobs(
        home_office_only=is_home_office,
        apenas_pcd=is_pcd,
        limit=target_count * 2  # Coleta margem extra para compensar já candidatadas
    )

    logging.info(f">> Total de vagas mapeadas: {len(collected_jobs)}")
    
    # Filtra as não candidatadas
    pending_jobs = [j for j in collected_jobs if not tracker.is_already_applied(j["link"])]
    logging.info(f">> Vagas inéditas disponíveis para aplicação: {len(pending_jobs)}")

    # Recupera progresso anterior se existir
    prev_home = 0
    prev_pcd = 0
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                prev_home = prev_data.get("home_office", {}).get("enviadas", 0)
                prev_pcd = prev_data.get("pcd", {}).get("enviadas", 0)
        except Exception:
            pass

    applied_count = prev_home if category_name == "home_office" else prev_pcd
    skipped_count = 0
    failed_count = 0

    for idx, job in enumerate(pending_jobs, 1):
        if applied_count >= target_count:
            logging.info(f"[META ATINGIDA] {target_count} candidaturas concluídas para {category_name}!")
            break

        title = job.get("titulo", "Vaga")
        company = job.get("empresa", "Empresa")
        url = job.get("link", "")

        logging.info(f"[{applied_count + 1}/{target_count}] Candidatando: '{title}' @ '{company}'")
        logging.info(f"    URL: {url}")

        try:
            res = await engine.apply_infojobs_job(url, dry_run=False)
            if res.get("sucesso"):
                applied_count += 1
                logging.info(f"    [SUCESSO] Candidatura enviada com sucesso! ({applied_count}/{target_count})")
            else:
                msg = res.get("mensagem", res.get("erro", "Falha"))
                logging.info(f"    [AVISO] {msg}")
                if "já foi candidatada" in str(msg).lower():
                    skipped_count += 1
                else:
                    failed_count += 1
        except Exception as e:
            logging.error(f"    [ERRO] Exceção durante envio: {e}")
            failed_count += 1

        # Atualiza arquivo de status
        if overall_progress is not None:
            overall_progress[category_name] = {
                "enviadas": applied_count,
                "meta": target_count,
                "concluido": applied_count >= target_count,
                "puladas": skipped_count,
                "falhas": failed_count,
                "ultima_vaga": title,
                "ultima_atualizacao": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            update_status(overall_progress)

        # Intervalo seguro para evitar bloqueio
        await asyncio.sleep(3.0)

    logging.info(f"[FIM DA CATEGORIA {category_name}] Enviadas: {applied_count} | Puladas: {skipped_count} | Falhas: {failed_count}")
    return applied_count

async def main():
    tracker = ApplicationsTracker()
    engine = JobBrowserEngine(headless=True)

    prev_home = 0
    prev_pcd = 0
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                prev_home = prev_data.get("home_office", {}).get("enviadas", 0)
                prev_pcd = prev_data.get("pcd", {}).get("enviadas", 0)
        except Exception:
            pass

    status_data = {
        "inicio": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "EM_EXECUCAO",
        "home_office": {"enviadas": prev_home, "meta": 300, "concluido": prev_home >= 300},
        "pcd": {"enviadas": prev_pcd, "meta": 300, "concluido": prev_pcd >= 300}
    }
    update_status(status_data)

    logging.info("=" * 75)
    logging.info(f"    RETOMANDO PIPELINE AUTO-APPLY: HOME OFFICE ({prev_home}/300) + PCD ({prev_pcd}/300)")
    logging.info("=" * 75)

    # Executa Categoria 1: 300 Vagas Home Office
    try:
        await process_target_category(
            category_name="home_office",
            target_count=300,
            engine=engine,
            tracker=tracker,
            is_home_office=True,
            is_pcd=False,
            overall_progress=status_data
        )
    except Exception as e:
        logging.error(f"Erro fatal na etapa Home Office: {e}")

    # Executa Categoria 2: 300 Vagas PcD
    try:
        await process_target_category(
            category_name="pcd",
            target_count=300,
            engine=engine,
            tracker=tracker,
            is_home_office=False,
            is_pcd=True,
            overall_progress=status_data
        )
    except Exception as e:
        logging.error(f"Erro fatal na etapa PcD: {e}")

    status_data["status"] = "CONCLUIDO"
    status_data["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
    update_status(status_data)
    logging.info("=" * 75)
    logging.info("    PIPELINE COMPLETO FINALIZADO COM SUCESSO!")
    logging.info("=" * 75)

if __name__ == "__main__":
    asyncio.run(main())
