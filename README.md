# Games

A small arcade of browser games, made for touch screens. Each game lives in its own folder with no build step. Most are a single self-contained HTML file; Hollowmarch also ships its art and sound files next to its `index.html`.

| Game | Folder | What it is |
| --- | --- | --- |
| Smash City | [`smash-city/`](smash-city/) | Climb and smash buildings as a giant monster while the army fights back. |
| Pyramid Hop | [`pyramid-hop/`](pyramid-hop/) | Hop around a cube pyramid to change every colour while dodging critters. |
| Vector Front | [`vector-front/`](vector-front/) | First-person wireframe tank battle with a TV-static camera look. |
| Naughts and Crosses | [`naughts-and-crosses/`](naughts-and-crosses/) | The classic, against an easy or unbeatable computer, or two players. |
| Hex Colour Balance | [`hex-colour-balance/`](hex-colour-balance/) | Place red, green and blue gems until each hexagon balances to white, across endless levels. |
| Massive Armies | [`massive-armies/`](massive-armies/) | 3D battle simulation with thousands of soldiers: formations, a tech tree and a 25-battle campaign. Uses WebGPU where available. |
| Hollowmarch | [`hollowmarch/`](hollowmarch/) | Tower defense: build and upgrade towers, lead two heroes and cast spells to hold the road across three stages. |

The root `index.html` is a landing page linking to all of them.

Massive Armies is built from its own repository, [Crunchy000/Battles](https://github.com/Crunchy000/Battles); `massive-armies/index.html` is a copy of that build. Its sounds include "Oculus Audio Pack 01" (CC BY 4.0), credited in the game's sound board, alongside CC0 recordings listed in the Battles README.

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

## Credits

Hollowmarch uses free CC0 assets by [Kenney](https://kenney.nl): Tower Defense Kit, Blocky Characters, Explosion Pack, Smoke Particles, Particle Pack, RPG Audio, Digital Audio, Impact Sounds, Interface Sounds, Sci-fi Sounds, Music Jingles and Voiceover packs.
