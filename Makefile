.PHONY: deploy

deploy:
	cd website && pnpm run build
	npx wrangler pages deploy website/build --project-name=zaquares
