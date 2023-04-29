import React from "react"
import {Main} from "./components/Main"
import { Route, Routes} from "react-router-dom";
import {InternalError} from "./components/500";
import {NotFound} from "./components/404";
import {NavMenu} from "./components/NavMenu";
import {Test} from "./components/Test";
import {TypeDescription} from "./components/TypeDescription";

function App() {
  return (
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
  );
}

export default App;
