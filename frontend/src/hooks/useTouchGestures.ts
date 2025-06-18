import { useGesture } from '@use-gesture/react';
import { useRef } from 'react';
import * as THREE from 'three';

export const useTouchGestures = (meshRef: React.RefObject<THREE.Mesh>) => {
  const initialRotationRef = useRef({ x: 0, y: 0 });
  const initialScaleRef = useRef(1);

  const bind = useGesture({
    onDrag: ({ offset: [x, y], first }) => {
      if (meshRef.current) {
        if (first) {
          initialRotationRef.current = {
            x: meshRef.current.rotation.x,
            y: meshRef.current.rotation.y,
          };
        }
        
        meshRef.current.rotation.y = initialRotationRef.current.y + x / 100;
        meshRef.current.rotation.x = initialRotationRef.current.x + y / 100;
        
        // Limit rotation to prevent disorientation
        meshRef.current.rotation.x = Math.max(
          -Math.PI / 2,
          Math.min(Math.PI / 2, meshRef.current.rotation.x)
        );
      }
    },
    
    onPinch: ({ offset: [scale], first }) => {
      if (meshRef.current) {
        if (first) {
          initialScaleRef.current = meshRef.current.scale.x;
        }
        
        const newScale = Math.max(0.5, Math.min(3, initialScaleRef.current * scale));
        meshRef.current.scale.setScalar(newScale);
      }
    },
    
    onDoubleClick: () => {
      // Reset to default view
      if (meshRef.current) {
        meshRef.current.rotation.set(0, 0, 0);
        meshRef.current.scale.setScalar(1);
        initialRotationRef.current = { x: 0, y: 0 };
        initialScaleRef.current = 1;
      }
    },
    
    onWheel: ({ delta: [, deltaY] }) => {
      // Handle mouse wheel for desktop
      if (meshRef.current) {
        const currentScale = meshRef.current.scale.x;
        const newScale = Math.max(0.5, Math.min(3, currentScale - deltaY * 0.001));
        meshRef.current.scale.setScalar(newScale);
      }
    },
  }, {
    drag: {
      threshold: 10,
    },
    pinch: {
      threshold: 0.1,
    },
  });

  const resetView = () => {
    if (meshRef.current) {
      meshRef.current.rotation.set(0, 0, 0);
      meshRef.current.scale.setScalar(1);
      initialRotationRef.current = { x: 0, y: 0 };
      initialScaleRef.current = 1;
    }
  };

  const setPresetView = (view: 'front' | 'back' | 'side') => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(1);
      
      switch (view) {
        case 'front':
          meshRef.current.rotation.set(0, 0, 0);
          break;
        case 'back':
          meshRef.current.rotation.set(0, Math.PI, 0);
          break;
        case 'side':
          meshRef.current.rotation.set(0, Math.PI / 2, 0);
          break;
      }
      
      initialRotationRef.current = {
        x: meshRef.current.rotation.x,
        y: meshRef.current.rotation.y,
      };
      initialScaleRef.current = 1;
    }
  };

  return {
    bind,
    resetView,
    setPresetView,
  };
}; 