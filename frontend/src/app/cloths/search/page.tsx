"use client";

import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import { useRouter } from "next/navigation";
import { useUser } from "@/app/UserContext";
import { AiFillLike, AiFillDislike } from "react-icons/ai";

interface ClothItem {
  id: number;
  name: string;
  price: number;
  image_url: string;
  colors_available: string;
  like_count: number;
  dislike_count: number;
}

export default function Page() {
  const [characters, setCharacters] = useState<ClothItem[]>([]);
  const { user } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push("/login");
      return;
    }

    fetch("http://127.0.0.1:8000/api/get-initial-cloth-items/")
      .then((res) => res.json())
      .then((data) => {
        const formattedData = data.map((item: any) => ({
          id: item.id,
          name: item.name,
          price: item.price,
          image_url: item.image_url,
          colors_available: item.colors_available,
          like_count: item.like_count,
          dislike_count: item.dislike_count,
        }));
        setCharacters(formattedData);
      });
  }, [user, router]);

  const swiped = (direction: string, nameToDelete: string) => {
    console.log("removing: " + nameToDelete);
    console.log("swiped: " + direction);
  };

  const outOfFrame = (name: string) => {
    console.log(name + " left the screen!");
  };

  return (
    <div>
      <h1>Clozyt</h1>
      <div className="cardContainer">
        {characters.map((character) => (
          <TinderCard
            className="swipe"
            key={character.name}
            onSwipe={(dir) => swiped(dir, character.name)}
            onCardLeftScreen={() => outOfFrame(character.name)}
          >
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
              <div
                style={{ backgroundImage: `url(${character.image_url})`, flex: 1 }}
                className="card"
              >
                <h3>{character.name}</h3>
              </div>
              <div className="counts-container" style={{ display: 'flex', flexDirection: 'column', marginLeft: '10px' }}>
                <div className="like-count" style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
                  <AiFillLike size={24} color="green" /> {character.like_count}
                </div>
                <div className="dislike-count" style={{ display: 'flex', alignItems: 'center' }}>
                  <AiFillDislike size={24} color="red" /> {character.dislike_count}
                </div>
              </div>
            </div>
          </TinderCard>
        ))}
      </div>
    </div>
  );
}
