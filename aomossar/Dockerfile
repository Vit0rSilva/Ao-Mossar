# ----------------------------------------
# ESTÁGIO 1: Construir (Build) o App Angular
# ----------------------------------------
# Usa uma imagem Node.js para compilar o projeto
FROM node:20-alpine AS build

# Define o diretório de trabalho
WORKDIR /app

# Copia o package.json e package-lock.json (para cache)
COPY package.json package-lock.json ./

# Instala as dependências (ci é mais rápido para deploys)
RUN npm ci

# Copia o resto do código-fonte
COPY . .

# Constrói o app para produção
# IMPORTANTE: Troque 'aomossar' pelo nome do seu projeto
# (O nome que aparece dentro da pasta 'dist/' após o build)
RUN npm run build -- --configuration production

# ----------------------------------------
# ESTÁGIO 2: Servir (Serve) os arquivos
# ----------------------------------------
# Usa uma imagem Nginx super leve para servir os arquivos estáticos
FROM nginx:alpine

# Copia os arquivos estáticos construídos no Estágio 1
# IMPORTANTE: Confirme que 'aomossar' é o nome da pasta em 'dist/'
COPY --from=build /app/dist/aomossar/browser /usr/share/nginx/html

# Copia a configuração customizada do Nginx (ver Passo 2)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expõe a porta 80 (padrão do Nginx)
EXPOSE 80