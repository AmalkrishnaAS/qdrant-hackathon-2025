'use client';
import React, { useEffect, useState } from 'react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { formatRegionLabel, REGION_LABELS } from '@/lib/regions';

const regions = ['US','IN','GB','DE','FR','JP','BR','CA','AU','AE'];

export default function SettingsPage() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [region, setRegion] = useState('US');
  const [count, setCount] = useState<number>(12);
  const [saving, setSaving] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const m = document.cookie.match(/(?:^|; )trending_region=([^;]+)/);
    if (m?.[1]) setRegion(decodeURIComponent(m[1]));
    const c = document.cookie.match(/(?:^|; )trending_count=([^;]+)/);
    if (c?.[1]) {
      const parsed = parseInt(decodeURIComponent(c[1]), 10);
      if (!Number.isNaN(parsed)) setCount(parsed);
    }
  }, []);

  const saveRegion = async () => {
    setSaving(true);
    try {
      await fetch('/api/settings/region', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region, count }),
      });
    } finally {
      setSaving(false);
    }
  };

  const saveCount = async () => {
    setSaving(true);
    try {
      await fetch('/api/settings/region', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region, count }),
      });
    } finally {
      setSaving(false);
    }
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen p-4 md:p-12 mt-20 max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="text-sm text-muted-foreground">Customize your experience</p>
      </div>

      <div className="divide-y rounded-lg border bg-card text-card-foreground">
        <div className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-medium">Theme</h2>
              <p className="text-xs text-muted-foreground">Choose your default appearance</p>
            </div>
            <div className="flex gap-2">
              <Button variant={resolvedTheme === 'light' ? 'default' : 'outline'} onClick={() => setTheme('light')}>Light</Button>
              <Button variant={resolvedTheme === 'dark' ? 'default' : 'outline'} onClick={() => setTheme('dark')}>Dark</Button>
              <Button variant={theme === 'system' ? 'default' : 'outline'} onClick={() => setTheme('system')}>System</Button>
            </div>
          </div>
        </div>
        <Separator />
        <div className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-medium">Trending Region</h2>
              <p className="text-xs text-muted-foreground">Used for YouTube most popular</p>
            </div>
            <div className="flex gap-2 items-center">
              <select
                className="border rounded-md px-3 py-2 bg-background"
                value={region}
                onChange={(e) => setRegion(e.target.value)}
              >
                {regions.map(r => <option key={r} value={r}>{formatRegionLabel(r)}</option>)}
              </select>
              <Button onClick={saveRegion} disabled={saving}>
                {saving ? 'Saving…' : 'Save'}
              </Button>
            </div>
          </div>
        </div>
        <Separator />
        <div className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-medium">Trending Count</h2>
              <p className="text-xs text-muted-foreground">How many trending items to show (1–50)</p>
            </div>
            <div className="flex gap-2 items-center">
              <input
                type="number"
                min={1}
                max={50}
                value={count}
                onChange={(e) => setCount(Math.max(1, Math.min(50, parseInt(e.target.value || '1', 10))))}
                className="w-24 border rounded-md px-3 py-2 bg-background"
              />
              <Button onClick={saveCount} disabled={saving}>
                {saving ? 'Saving…' : 'Save'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


