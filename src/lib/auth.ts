import { createClient } from '@supabase/supabase-js';
import { auth as webcontainerAuth } from '@webcontainer/api';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Missing Supabase configuration in environment variables');
}

// Secure Storage Handler with frame origin protection
class SecureStorage {
  private static verifyOrigin() {
    if (window.self !== window.top) {
      throw new Error('Cross-origin frame access denied');
    }
  }

  static getItem(key: string): string | null {
    try {
      this.verifyOrigin();
      return localStorage.getItem(key);
    } catch (error) {
      console.warn('Storage access blocked:', error);
      return null;
    }
  }

  static setItem(key: string, value: string): void {
    try {
      this.verifyOrigin();
      localStorage.setItem(key, value);
    } catch (error) {
      console.warn('Storage write blocked:', error);
    }
  }

  static removeItem(key: string): void {
    try {
      this.verifyOrigin();
      localStorage.removeItem(key);
    } catch (error) {
      console.warn('Storage removal blocked:', error);
    }
  }
}

// Frame-Secure Supabase Client
export const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: true,
    detectSessionInUrl: false,
    storage: SecureStorage,
    flowType: 'pkce'
  },
  global: {
    fetch: (input, init) => {
      // Block any iframe-related requests
      if (typeof input === 'string' && 
          (input.includes('iframe') || 
           input.includes('webcontainer') ||
           input.includes('cross-origin'))) {
        throw new Error('Frame-based requests blocked for security');
      }
      return fetch(input, {
        ...init,
        credentials: 'same-origin',
        mode: 'same-origin'
      });
    }
  }
});

// Global Fetch Interceptor
const originalFetch = window.fetch;
window.fetch = async function(input: RequestInfo | URL, init?: RequestInit) {
  // Block cross-origin iframe requests
  if (window.self !== window.top) {
    throw new Error('Cross-origin fetch requests not allowed');
  }

  const secureInit = {
    ...init,
    credentials: 'same-origin',
    mode: 'same-origin',
    headers: {
      ...init?.headers,
      'Cross-Origin-Embedder-Policy': 'credentialless',
      'Cross-Origin-Opener-Policy': 'same-origin',
      'X-Frame-Options': 'DENY'
    }
  };

  return originalFetch.call(window, input, secureInit);
};

// Auth functions with frame protection
export async function signUp(email: string, password: string, username: string) {
  if (window.self !== window.top) {
    throw new Error('Auth operations not allowed in frames');
  }
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: { data: { username } }
  });
  if (error) throw error;
  return data;
}

export async function signIn(email: string, password: string) {
  if (window.self !== window.top) {
    throw new Error('Auth operations not allowed in frames');
  }
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });
  if (error) throw error;
  return data;
}

export async function signOut() {
  if (window.self !== window.top) {
    throw new Error('Auth operations not allowed in frames');
  }
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

// WebContainer Auth Initialization
export async function initializeWebContainerAuth(clientId: string) {
  try {
    if (window.self !== window.top) {
      throw new Error('WebContainer auth must run in top frame');
    }
    
    const result = await webcontainerAuth.init({
      clientId,
      scope: 'policy-simulator',
      editorOrigin: window.location.origin,
      credentialless: true
    });
    
    return result;
  } catch (error) {
    console.error('WebContainer auth failed:', error);
    return { status: 'error', error };
  }
}
