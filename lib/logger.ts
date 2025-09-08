type LogMeta = Record<string, unknown> | undefined;

export function logError(message: string, error?: unknown, meta?: LogMeta): void {
  const payload = {
    level: 'error',
    message,
    error: serializeError(error),
    ...(meta ? { meta } : {}),
  };
  // eslint-disable-next-line no-console
  console.error(formatPayload(payload));
}

export function logWarn(message: string, meta?: LogMeta): void {
  const payload = {
    level: 'warn',
    message,
    ...(meta ? { meta } : {}),
  };
  // eslint-disable-next-line no-console
  console.warn(formatPayload(payload));
}

export function logInfo(message: string, meta?: LogMeta): void {
  const payload = {
    level: 'info',
    message,
    ...(meta ? { meta } : {}),
  };
  // eslint-disable-next-line no-console
  console.info(formatPayload(payload));
}

function serializeError(error: unknown): Record<string, unknown> | undefined {
  if (!error) return undefined;
  if (error instanceof Error) {
    return {
      name: error.name,
      message: error.message,
      stack: error.stack,
    
      status: (error as any)?.status,
      data: (error as any)?.data,
    };
  }
  try {
    return { value: JSON.stringify(error) };
  } catch {
    return { value: String(error) };
  }
}

function formatPayload(payload: Record<string, unknown>): string {
  try {
    return `[app] ${new Date().toISOString()} ${JSON.stringify(payload)}`;
  } catch {
    return `[app] ${new Date().toISOString()} ${String(payload.message ?? 'log')}`;
  }
}


