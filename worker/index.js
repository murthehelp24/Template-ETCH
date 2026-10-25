// Password gate in front of the Page Builder's static files (wrangler.jsonc: assets.run_worker_first = true,
// so every request — pages, scripts, preview frames — passes through here first).
//
// The password is the Worker secret BUILDER_PASSWORD (Cloudflare dashboard → Worker → Settings →
// Variables and Secrets). Without it every request is refused, so a deploy can never open the site by accident.
// Browsers ask once per session with their own login box (HTTP Basic auth); the user name is not checked.

const REALM = 'Etch Page Builder';

export default {
  async fetch(request, env) {
    const password = env.BUILDER_PASSWORD;
    if (!password) {
      return text(503, 'Page Builder is locked: set the BUILDER_PASSWORD secret on this Worker.');
    }
    if (!(await authorised(request.headers.get('Authorization'), password))) {
      return text(401, 'Password required.', {
        'WWW-Authenticate': `Basic realm="${REALM}", charset="UTF-8"`,
      });
    }
    const res = await env.ASSETS.fetch(request);
    const out = new Response(res.body, res);
    out.headers.set('Cache-Control', 'private, no-cache'); // never kept by shared caches
    return out;
  },
};

async function authorised(header, password) {
  const match = /^Basic\s+([A-Za-z0-9+/=]+)$/i.exec(header || '');
  if (!match) return false;
  let decoded;
  try {
    decoded = new TextDecoder().decode(Uint8Array.from(atob(match[1]), (c) => c.charCodeAt(0)));
  } catch {
    return false;
  }
  const given = decoded.slice(decoded.indexOf(':') + 1);
  // compare digests of equal length in constant time, so response timing does not leak the password
  const [a, b] = await Promise.all([digest(given), digest(password)]);
  return crypto.subtle.timingSafeEqual(a, b);
}

async function digest(value) {
  return crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
}

function text(status, body, headers = {}) {
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Robots-Tag': 'noindex, nofollow',
      ...headers,
    },
  });
}
