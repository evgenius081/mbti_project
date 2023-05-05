import React, {useState, useMemo} from "react"
import {Main} from "./components/Main"
import { Route, Routes} from "react-router-dom";
import {InternalError} from "./components/500";
import {NotFound} from "./components/404";
import {NavMenu} from "./components/NavMenu";
import {Test} from "./components/Test";
import {TypeDescription} from "./components/TypeDescription";
import {Context} from "./context"

function App() {
    const [mbtiTypes, setMbtiTypes] = useState({"IE": [0, 0], "NS": [0, 0],
        "TF": [0, 0], "JP": [0, 0]})

    const value = useMemo(
        () => ({ mbtiTypes, setMbtiTypes }),
        [mbtiTypes]
    );
    return (
      <Context.Provider value={value}>
          {useMemo(() => (
              <>
            <NavMenu />
            <Routes>
                <Route exact path='/' element={<Main/>} />
                <Route exact path='types/test' element={<Test />} />
                <Route exact path='/error' element={<InternalError />}/>
                <Route exact path='/not-found' element={<NotFound />}/>
                <Route exact path='/types/:type' element={<TypeDescription/>}/>
                <Route path='*' element={<NotFound />} />
            </Routes>
              </>
          ), [])}
      </Context.Provider>
  );
}

export default App;
