import React, { createContext, useState } from 'react';

export const DbContext = createContext();

export const DbProvider = ({ children }) => {
    const [dbName, setDbName] = useState("Define DB name");
    return (
        <DbContext.Provider value={{ dbName, setDbName }}>
            {children}
        </DbContext.Provider>
    );
};
