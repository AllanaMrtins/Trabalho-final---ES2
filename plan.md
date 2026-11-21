# Redesign gamificado — Afim Quest

## Objetivo

Atualizar a interface existente de ensino de função afim para uma experiência gamificada com ritmo editorial e sensação de evento, inspirada apenas em padrões gerais observados na referência fornecida: hero com chamada forte, blocos de conteúdo, navegação por seções e chamadas de ação. A identidade visual será própria.

## Direção visual escolhida

- **Movimento:** editorial digital com energia de festival de tecnologia e interface de missão.

- **Princípios:** foco no próximo passo, contraste alto com fundos escuros, conteúdo em cartões leves e feedback visual imediato.

- **Paleta:** azul-noite como base; verde-lima como cor proprietária de progresso; coral para ação; creme para leitura; violeta apenas como apoio.

- **Layout:** cabeçalho compacto, hero assimétrico e áreas de conteúdo com cartões responsivos; no mobile, navegação horizontal rolável.

- **Elementos de assinatura:** marca “AQ” em selo circular, trilhas pontilhadas de progresso e etiquetas de missão com nível/XP.

- **Interação:** toda ação importante comunica estado, XP, acerto/erro e próximo passo; hover e foco são discretos e acessíveis.

- **Animação:** entrada suave por elevação, brilho curto em acerto e movimento sutil de progresso; sem animações contínuas pesadas.

- **Tipografia:** Manrope para leitura e Space Grotesk para títulos, com pesos contrastantes.

- **Essência:** uma sala de treino digital para aprender função afim como quem avança por fases — prática, clara e motivadora.

- **Voz:** direta, encorajadora e orientada a ação. Exemplos: “Escolha sua próxima missão.” / “Cada acerto muda seu nível.”

- **Marca:** selo “AQ” + wordmark Afim Quest, com um traço inclinado lembrando uma reta cartesiana.

- **Cor proprietária:** verde-lima `#C8F36A`, usado em progresso e conquistas.

## Implementação

- Preservar a API, autenticação e todas as rotas atuais.

- Reescrever o sistema visual em `app/static/index.html`, mantendo as funções JavaScript existentes.

- Adicionar manifest de rotas em `public/manus-routes.json`.

- Validar sintaxe Python e executar a suíte de testes existente.