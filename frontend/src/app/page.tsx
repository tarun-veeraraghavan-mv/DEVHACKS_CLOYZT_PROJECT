"use client";
import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";

interface ClothItem {
  name: string;
  url: string;
}

export default function Home() {
  const [characters, setCharacters] = useState<ClothItem[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/get-initial-cloth-items/")
      .then((res) => res.json())
      .then((data) => {
        const formattedData = data.map((item: any) => ({
          name: item.name,
          url: item.image_url,
        }));
        setCharacters(formattedData);
      });
  }, []);

  const swiped = (direction: string, nameToDelete: string) => {
    console.log("removing: " + nameToDelete);
    console.log("swiped: " + direction);
  };

  const outOfFrame = (name: string) => {
    console.log(name + " left the screen!");
  };

  return (
    <div>
      <link
        href="https://fonts.googleapis.com/css?family=Damion&display=swap"
        rel="stylesheet"
      />
      <link
        href="https://fonts.googleapis.com/css?family=Alatsi&display=swap"
        rel="stylesheet"
      />
      <h1>Clozyt</h1>
      <div className="cardContainer">
        {characters.map((character) => (
          <TinderCard
            className="swipe"
            key={character.name}
            onSwipe={(dir) => swiped(dir, character.name)}
            onCardLeftScreen={() => outOfFrame(character.name)}
          >
            <div
              style={{ backgroundImage: `url(${character.url})` }}
              className="card"
            >
              <h3>{character.name}</h3>
            </div>
          </TinderCard>
        ))}
      </div>
    </div>
  );
}

