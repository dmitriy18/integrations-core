FROM node:alpine
RUN apk add git jq python3 --no-cache
RUN npm install -g ts-node
RUN npm install typescript @typescript-eslint/parser @typescript-eslint/typescript-estree @types/node
RUN pip3 install pyyaml
COPY parse_ts.ts /scripts/parse_ts.ts
COPY validate_log_intgs.py /scripts/validate_log_intgs.py