import { Routes } from '@angular/router';
import { Inicial } from './componentes/inicial/inicial';
import { Component } from '@angular/core';
import { Horarios } from './componentes/horarios/horarios';


export const routes: Routes = [
    { path: '', component: Inicial},
    { path: 'cardapios', component: Horarios }
];
