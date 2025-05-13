import { json } from '@remix-run/node';
import type { LoaderFunction } from '@remix-run/node';
import { verifyToken, extractTokenFromHeader } from '~/lib/jwt';
import { supabase } from '~/lib/auth';

interface AuthPayload {
  userId: string;
  role?: string;
  sessionId?: string;
}

export const loader: LoaderFunction = async ({ request }) => {
  try {
    // Extract and validate token
    const authHeader = request.headers.get('Authorization');
    const token = extractTokenFromHeader(authHeader);
    
    if (!token) {
      return json(
        { error: 'Authorization token required' }, 
        { status: 401 }
      );
    }

    // Verify token with strict typing
    const payload = verifyToken(token) as AuthPayload;
    
    // Fetch user profile from Supabase
    const { data: profile, error } = await supabase
      .from('profiles')
      .select('id, username, full_name, avatar_url, roles')
      .eq('id', payload.userId)
      .single();

    if (error || !profile) {
      return json(
        { error: 'User profile not found' },
        { status: 404 }
      );
    }

    // Return minimal required user data
    return json({
      user: {
        id: payload.userId,
        email: profile.username + '@example.com',
        username: profile.username,
        name: profile.full_name,
        avatar: profile.avatar_url,
        roles: profile.roles || []
      },
      session: payload.sessionId
    });

  } catch (error) {
    console.error('Auth loader error:', error);
    
    return json(
      { 
        error: 'Authentication failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 401 }
    );
  }
};
