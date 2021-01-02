# Neat-rex
A small neat ai learning how to play chromium t-rex runner<br/>

NeuroEvolution of Augmenting Topologies is a genetic algorithm<br/>
for the generation of evolving artificial neural networks developed by Ken Stanley in 2002.<br/>

I started with a population of 25 t-rex, fitness for each individual is equal to score.<br/>
Fitness threshold is equal to 10 so whenever an individual reaches score 10, the simulation runs up<br/>
to the point where all t-rex are extinguished and doesn't repeat itself. After that, a winner.pkl file<br/>
is created with the champion genome.

It is used one parameter as input which is the distance between t-rex and next cactus and neat generates<br/>
two outputs which are used as criteria to jump or not.

## Demo

![alt text](https://github.com/caiovini/Neat-rex/blob/main/Demo.gif)

## Requirement

python 3.8

## Instructions

install requirements: "pip3 install -r requirements"<br/>
                 run: "python3 game.py"

## Resources 

Assets for this game can be found [Here!](https://github.com/wayou/t-rex-runner/tree/gh-pages/assets)

