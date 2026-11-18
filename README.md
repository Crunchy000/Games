# Games

A small arcade of browser games, made for touch screens. Each game is a single self-contained HTML file with no build step and no dependencies.

| Game | Folder | What it is |
| --- | --- | --- |
| Smash City | [`smash-city/`](smash-city/) | Climb and smash buildings as a giant monster while the army fights back. |
| Pyramid Hop | [`pyramid-hop/`](pyramid-hop/) | Hop around a cube pyramid to change every colour while dodging critters. |
| Vector Front | [`vector-front/`](vector-front/) | First-person wireframe tank battle with a TV-static camera look. |
| Naughts and Crosses | [`naughts-and-crosses/`](naughts-and-crosses/) | The classic, against an easy or unbeatable computer, or two players. |
| Hex Colour Balance | [`hex-colour-balance/`](hex-colour-balance/) | Place red, green and blue gems until each hexagon balances to white, across endless levels. |

The root `index.html` is a landing page linking to all of them.

## Controls

- **Touch:** drag to move, tap to act. Each game shows its controls on the title screen.
- **Keyboard:** arrow keys or WASD, plus space.

## Hosting on GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch**, Branch: **main**, folder **/ (root)**.
The site will then be at `https://<user>.github.io/Games/`. The empty `.nojekyll` file tells Pages to serve the files as they are.

## Running locally

Open any `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```
