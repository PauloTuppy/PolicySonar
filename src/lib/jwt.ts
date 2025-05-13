import { sign, verify, decode, JwtPayload, SignOptions } from 'jsonwebtoken';
import { env } from './env';

// Strongly typed JWT payload
export interface JWTPayload extends JwtPayload {
  userId: string;
  role?: string;
  sessionId?: string;
}

// Token configuration
const TOKEN_CONFIG = {
  access: {
    expiresIn: '15m', // Short-lived access token
    type: 'access'
  },
  refresh: {
    expiresIn: '7d', // Long-lived refresh token
    type: 'refresh'
  }
} as const;

// Validate environment variable
if (!env.JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is not set');
}

// Create signed token with type safety
export function createToken(
  payload: Omit<JWTPayload, 'iat' | 'exp'>,
  tokenType: keyof typeof TOKEN_CONFIG
): string {
  const options: SignOptions = {
    ...TOKEN_CONFIG[tokenType],
    algorithm: 'HS256',
    issuer: 'policy-sonar',
    audience: ['web', 'mobile']
  };

  return sign(payload, env.JWT_SECRET, options);
}

// Verify token with comprehensive checks
export function verifyToken(token: string): JWTPayload {
  try {
    const decoded = verify(token, env.JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'policy-sonar',
      audience: ['web', 'mobile']
    }) as JWTPayload;

    if (!decoded.userId) {
      throw new Error('Invalid token payload');
    }

    return decoded;
  } catch (error) {
    throw new Error('Invalid or expired token');
  }
}

// Safe token decoding (without verification)
export function decodeToken(token: string): JWTPayload | null {
  try {
    const decoded = decode(token) as JWTPayload | null;
    return decoded;
  } catch {
    return null;
  }
}

// Extract token from authorization header
export function extractTokenFromHeader(authHeader: string | undefined): string | null {
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }

  const token = authHeader.substring(7).trim();
  return token || null;
}

// Token utilities for specific use cases
export const TokenUtils = {
  createAccessToken: (payload: Omit<JWTPayload, 'iat' | 'exp'>) =>
    createToken(payload, 'access'),
  createRefreshToken: (payload: Omit<JWTPayload, 'iat' | 'exp'>) =>
    createToken(payload, 'refresh'),
  verifyAccessToken: verifyToken,
  verifyRefreshToken: verifyToken
};
