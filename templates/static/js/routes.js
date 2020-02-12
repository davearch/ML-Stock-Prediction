import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';
import AssetForm from './components/AssetForm';

// import more components
export default (
    <HashRouter history={hashHistory}>
     <div>
      <Route path='/' component={ AssetForm } />
     </div>
    </HashRouter>
);
