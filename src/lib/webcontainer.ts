import { WebContainer } from '@webcontainer/api';
import { WORK_DIR_NAME } from './constants';
import { initializeWebContainerAuth } from '../auth';

// WebContainer instance with type safety
let webcontainerInstance: Promise<WebContainer> | null = null;

// WebContainer context with strict typing
interface WebContainerContext {
  loaded: boolean;
  ready: Promise<void>;
  resolveReady: () => void;
}

export const webcontainerContext: WebContainerContext = {
  loaded: false,
  ready: new Promise((resolve) => {
    (webcontainerContext as any).resolveReady = resolve;
  }),
} as WebContainerContext;

// Secure WebContainer initialization
export async function initializeWebContainer() {
  if (typeof window === 'undefined') return; // Skip in SSR
  
  try {
    // Initialize auth before booting WebContainer
    const authResult = await initializeWebContainerAuth('policy-simulator-client');
    if (authResult.status === 'error') {
      throw new Error('WebContainer auth initialization failed');
    }

    // Use existing instance if available (HMR support)
    if (!webcontainerInstance) {
      webcontainerInstance = WebContainer.boot({
        coep: 'credentialless',
        workdirName: WORK_DIR_NAME,
        forwardPreviewErrors: true,
        // Additional security constraints
        rejectIframeAttacks: true,
        disableEmbeddedAPI: true
      }).then(async (instance) => {
        webcontainerContext.loaded = true;
        webcontainerContext.resolveReady();
        
        // Mount initial file system if needed
        await ensureDefaultFilesystem(instance);
        
        return instance;
      });
    }

    return webcontainerInstance;
  } catch (error) {
    console.error('WebContainer initialization failed:', error);
    throw new Error('Failed to initialize WebContainer');
  }
}

// Helper function to ensure default filesystem structure
async function ensureDefaultFilesystem(instance: WebContainer) {
  try {
    const files = await instance.fs.readdir(WORK_DIR_NAME);
    if (files.length === 0) {
      await instance.fs.mkdir(`${WORK_DIR_NAME}/logs`);
      await instance.fs.writeFile(
        `${WORK_DIR_NAME}/README.md`,
        '# PolicySonar Workspace\n\nThis is your secure workspace.'
      );
    }
  } catch (error) {
    console.warn('Filesystem initialization failed:', error);
  }
}

// Get WebContainer instance with safety checks
export async function getWebContainer(): Promise<WebContainer> {
  if (!webcontainerInstance) {
    throw new Error('WebContainer not initialized - call initializeWebContainer() first');
  }
  
  await webcontainerContext.ready;
  return webcontainerInstance;
}

// Initialize on module load (with error boundary)
if (typeof window !== 'undefined') {
  initializeWebContainer().catch((error) => {
    console.error('Critical WebContainer init error:', error);
    webcontainerContext.loaded = false;
  });
}
