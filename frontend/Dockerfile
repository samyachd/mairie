# ═══════════════════════════════════════════════════════════
# Stage commun : base avec les dépendances installées
# ═══════════════════════════════════════════════════════════
FROM node:24-alpine AS deps

WORKDIR /app

# On copie d'abord UNIQUEMENT les fichiers de dépendances
# pour maximiser le cache Docker (comme avec pyproject.toml côté backend)
COPY package*.json ./

# npm ci est plus strict et plus rapide que npm install
# Il exige un package-lock.json et installe exactement ce qui est dedans
RUN npm ci


# ═══════════════════════════════════════════════════════════
# Stage DEV : serveur Vite avec hot-reload
# ═══════════════════════════════════════════════════════════
FROM deps AS dev

# On récupère le code source par-dessus les deps
# (en dev c'est "poli" mais le vrai code viendra du bind mount)
COPY . .

EXPOSE 5173

# Vite en mode dev, écoute toutes les interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# ═══════════════════════════════════════════════════════════
# Stage BUILDER : compile le bundle de production
# ═══════════════════════════════════════════════════════════
FROM deps AS builder

# Récupère le code source
COPY . .

# On déclare l'arg au moment où on en a besoin
# puis on le convertit en ENV pour que Vite le capte
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build statique : génère /app/dist
RUN npm run build


# ═══════════════════════════════════════════════════════════
# Stage PROD : nginx léger qui sert le build
# ═══════════════════════════════════════════════════════════
FROM nginx:alpine AS prod

# Copie du build depuis le stage "builder"
# (c'est LA magie du multi-stage : on prend juste ce qu'on veut)
COPY --from=builder /app/dist /usr/share/nginx/html

# Notre config personnalisée remplace la config par défaut
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# nginx tourne en foreground (pas en daemon) pour que Docker
# puisse gérer son cycle de vie
CMD ["nginx", "-g", "daemon off;"]