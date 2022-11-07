

#!/bin/bash
pushd "$(dirname "$0")"

python generate_middleware_code.py fragment > ../front/src/gql/traefik/MiddlewareFragment.graphql
python generate_middleware_code.py mutation > ../front/src/gql/traefik/MiddlewareMutations.js
python generate_middleware_code.py json | tee ../back/app/traefik/middlewares.json > ../front/src/components/Traefik/Middleware/definitions.json
python generate_middleware_code.py schema > ../back/schema/traefik/middlewares.graphql
popd