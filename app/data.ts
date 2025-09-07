import { IconMusic } from "@tabler/icons-react";
import React from 'react';

interface Item {
  title: string;
  category: string;
  description: string;
  link: string;
  icon: React.ReactNode;
}

export const items: Item[] = [
  {
    title: "Bohemian Rhapsody",
    category: "Queen",
    description: "A six-minute suite, notable for its lack of a refraining chorus and instead consisting of several sections",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-rose-500" }),
  },
  {
    title: "Blinding Lights",
    category: "The Weeknd",
    description: "A synth-pop and nu-disco song with a pulsing beat and retro 1980s feel",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-purple-500" }),
  },
  {
    title: "Don't Start Now",
    category: "Dua Lipa",
    description: "A disco-pop and nu-disco song with elements of 1970s disco and 1980s pop",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-blue-500" }),
  },
  {
    title: "Watermelon Sugar",
    category: "Harry Styles",
    description: "A pop rock and soft rock song with elements of funk and psychedelic pop",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-red-500" }),
  },
  {
    title: "Levitating",
    category: "Dua Lipa ft. DaBaby",
    description: "A disco-pop and dance-pop song with elements of 1970s and 1980s dance music",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-pink-500" }),
  },
  {
    title: "Save Your Tears",
    category: "The Weeknd",
    description: "A synth-pop and new wave song with a retro 1980s feel",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-indigo-500" }),
  },
  {
    title: "Stay",
    category: "The Kid LAROI, Justin Bieber",
    description: "A pop and emo rap song with a melancholic yet catchy melody",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-green-500" }),
  },
  {
    title: "good 4 u",
    category: "Olivia Rodrigo",
    description: "A pop-punk and pop-rock song with angsty lyrics and energetic instrumentals",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-yellow-500" }),
  },
  {
    title: "Montero",
    category: "Lil Nas X",
    description: "A pop-rap and trap song with Middle Eastern influences and provocative lyrics",
    link: "#",
    icon: React.createElement(IconMusic, { className: "h-full text-orange-500" }),
  },
];
