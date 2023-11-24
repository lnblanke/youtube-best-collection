import "./App.css";
import {Navigate, Route, Routes, Router} from 'react-router-dom';
import Register from './register'
import Login from './login'
import Home from './home'

const App = () => {
  return (
      <>
        <Routes>
          <Route path = {"/register"} element = {<Register/>}/>
          <Route path = {"/login"} element = {<Login/>}/>
          <Route path = {"/home"} element = {<Home/>}/>
          <Route path = {"/"} element = {<Navigate to = {"/home"}/>}/>
        </Routes>
      </>
  );
}

export default App;