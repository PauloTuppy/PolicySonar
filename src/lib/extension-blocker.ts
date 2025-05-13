// Enhanced extension blocker with additional security measures
export function blockExtensions() {
  if (typeof window === 'undefined') return;

  // Block common extension property access
  const originalDescriptor = Object.getOwnPropertyDescriptor(window, 'origin');
  Object.defineProperty(window, 'origin', {
    get: function() {
      return originalDescriptor?.get?.call(window) || window.location.origin;
    },
    configurable: false,
    enumerable: true
  });

  // Block known extension properties
  const blockedProperties = [
    'ethereum',
    'web3',
    'solana',
    'phantom',
    'trustwallet'
  ];

  blockedProperties.forEach(prop => {
    Object.defineProperty(window, prop, {
      configurable: false,
      writable: false,
      value: undefined
    });
  });

  // Freeze critical objects
  Object.freeze(window.location);
  Object.freeze(Object.prototype);
}

// Initialize immediately
if (typeof window !== 'undefined') {
  blockExtensions();
}
