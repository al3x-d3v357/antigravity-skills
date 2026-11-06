import sys
import argparse
import threads_poster
import instagram_poster
import x_poster
import tiktok_poster
import trend_analyzer


def main():
    parser = argparse.ArgumentParser(description="Social Auto-Post - Publicador Multi-Plataforma com Análise de Tendências do Exterior")
    parser.add_argument("--platform", choices=["threads", "instagram", "insta", "x", "twitter", "tiktok"], default="threads", help="Plataforma de destino: threads, instagram, x ou tiktok (Padrão: threads)")
    parser.add_argument("--login", action="store_true", help="Abre o navegador ou executa SSO para autenticar a plataforma escolhida")
    parser.add_argument("--analyze-only", action="store_true", help="Executa apenas a análise de tendências internacionais (tags, música e legenda)")
    parser.add_argument("--live-trends", action="store_true", help="Consulta as páginas do exterior ao vivo antes de postar")
    parser.add_argument("--post", type=str, help="Texto ou legenda da postagem (SEM emojis)")
    parser.add_argument("--hashtags", type=str, default="", help="Hashtags contextuais separadas por espaço")
    parser.add_argument("--media", nargs="+", help="Caminhos de imagens ou vídeos renderizados")
    parser.add_argument("--video", type=str, help="Caminho do arquivo de vídeo (específico para TikTok)")
    parser.add_argument("--visible", action="store_true", help="Executa o navegador de forma visível")
    parser.add_argument("--history", action="store_true", help="Mostra histórico da plataforma")

    args = parser.parse_args()
    platform = args.platform.lower()

    if args.analyze_only:
        report = trend_analyzer.analyze_and_adapt(args.post or "", args.hashtags, args.media, live=args.live_trends)
        trend_analyzer.print_trend_report(report)
        return

    if platform in ["instagram", "insta"]:
        if args.login:
            instagram_poster.interactive_login()
        elif args.history:
            instagram_poster.show_history()
        elif args.post:
            instagram_poster.post_instagram(args.post, args.media, hashtags=args.hashtags, headless=not args.visible, live_trends=args.live_trends)
        else:
            parser.print_help()

    elif platform in ["x", "twitter"]:
        if args.login:
            x_poster.interactive_login()
        elif args.history:
            x_poster.show_history()
        elif args.post:
            report = trend_analyzer.analyze_and_adapt(args.post, args.hashtags, args.media)
            full_text = f"{report['adapted_caption_zero_emojis']}\n\n{report['recommended_international_hashtags']}".strip()
            x_poster.post_x(full_text, args.media, headless=not args.visible)
        else:
            parser.print_help()

    elif platform == "tiktok":
        if args.login:
            tiktok_poster.interactive_login()
        elif args.history:
            tiktok_poster.show_history()
        elif args.post or args.video or (args.media and len(args.media) > 0):
            video_file = args.video if args.video else (args.media[0] if args.media else None)
            if not video_file:
                print("ERRO: O TikTok requer um arquivo de vídeo (--video ou --media).")
                return
            report = trend_analyzer.analyze_and_adapt(args.post or "", args.hashtags, [video_file])
            full_text = f"{report['adapted_caption_zero_emojis']}\n\n{report['recommended_international_hashtags']}".strip()
            tiktok_poster.post_tiktok(full_text, video_file, headless=not args.visible)
        else:
            parser.print_help()

    else:
        # Padrão Threads (Instagram)
        if args.login:
            threads_poster.interactive_login()
        elif args.history:
            threads_poster.show_history()
        elif args.post:
            threads_poster.post_thread(args.post, hashtags=args.hashtags, media_paths=args.media, headless=not args.visible, live_trends=args.live_trends)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
