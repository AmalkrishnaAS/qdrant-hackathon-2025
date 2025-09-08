import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { region, count } = await request.json().catch(() => ({}));
  if (!region || typeof region !== 'string' || region.length !== 2) {
    return NextResponse.json({ ok: false, error: 'Invalid region' }, { status: 400 });
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set('trending_region', region.toUpperCase(), {
    path: '/',
    maxAge: 60 * 60 * 24 * 365,
    sameSite: 'lax',
  });
  if (typeof count === 'number' && count >= 1 && count <= 50) {
    res.cookies.set('trending_count', String(count), {
      path: '/',
      maxAge: 60 * 60 * 24 * 365,
      sameSite: 'lax',
    });
  }
  return res;
}


