import { createContext, useContext, useState } from "react";

const AppContext = createContext<any>(null);

export const AppProvider = ({ children }: any) => {
  const [token, setToken] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);

  return (
    <AppContext.Provider value={{ token, setToken, taskId, setTaskId }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppState = () => useContext(AppContext);

