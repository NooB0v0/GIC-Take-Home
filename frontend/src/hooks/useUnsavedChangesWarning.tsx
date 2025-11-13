import { useCallback, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';


const useUnsavedChangesWarning = (isDirty: boolean) => {
  const [isFormSaved, setIsFormSaved] = useState(false);
  const location = useLocation();

  const saveForm = useCallback(() => setIsFormSaved(true), []);
  const resetForm = useCallback(() => setIsFormSaved(false), []);
  
  useEffect(() => {
    const message = "You have unsaved changes. Are you sure you want to leave?";

    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty && !isFormSaved) {
        e.returnValue = message;
        return message;
      }
    };

    if (isDirty && !isFormSaved) {
      window.addEventListener('beforeunload', handleBeforeUnload);
    } else {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    }

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [isDirty, isFormSaved, location]);

  return [isDirty && !isFormSaved, saveForm, resetForm] as const;
};

export default useUnsavedChangesWarning;