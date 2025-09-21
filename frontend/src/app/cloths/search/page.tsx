"use client";

import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import { useRouter } from "next/navigation";
import { useUser } from "@/app/UserContext";
import { AiFillLike, AiFillDislike } from "react-icons/ai";
import axios from "axios";

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
          price: Number(item.price),
          image_url: item.image_url,
          colors_available: item.colors_available,
          like_count: item.like_count,
          dislike_count: item.dislike_count,
        }));
        setCharacters(formattedData);
      });
  }, [user, router]);

  const BASE_URL = "http://127.0.0.1:8000"; // Assuming your backend is running on this URL

  const handleSwipe = async (itemId: number, direction: "left" | "right") => {
    try {
      const { data: newItem } = await axios.post<ClothItem>(
        `${BASE_URL}/api/swipe/`,
        {
          item_id: itemId,
          user_id: 7,
          direction: direction,
        }
      );

      console.log("New item received:", newItem);
      if (newItem && newItem.id) {
        setCharacters((prev) => [...prev, { ...newItem, price: Number(newItem.price) }]);
      }
    } catch (error) {
      console.error("Error sending swipe request:", error);
    }
  };

  const swiped = (direction: string, itemId: number, nameToDelete: string) => {
    console.log("removing: " + nameToDelete);
    setCharacters((prev) => prev.filter((c) => c.id !== itemId));
    handleSwipe(itemId, direction === "right" ? "right" : "left");
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
            key={character.id}
            onSwipe={(dir) => {
              console.log(
                "swiped " +
                  dir +
                  " for " +
                  character.name +
                  " id: " +
                  character.id
              );
              swiped(dir, character.id, character.name);
            }}
            onCardLeftScreen={() => outOfFrame(character.name)}
          >
            <div
              className="card"
              style={{
                position: "relative",
                width: "350px",
                height: "500px",
                backgroundImage: `url(${character.image_url})`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                borderRadius: "20px",
                boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.2)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
              }}
            >
              <div
                className="counts-container"
                style={{
                  display: "flex",
                  justifyContent: "space-around",
                  padding: "10px",
                  backgroundColor: "rgba(0, 0, 0, 0.4)",
                  borderTopLeftRadius: "20px",
                  borderTopRightRadius: "20px",
                  color: "white",
                }}
              >
                <div
                  className="like-count"
                  style={{ display: "flex", alignItems: "center" }}
                >
                  <AiFillLike size={24} color="lightgreen" />
                  <span style={{ marginLeft: "5px" }}>
                    {character.like_count}
                  </span>
                </div>
                <div
                  className="dislike-count"
                  style={{ display: "flex", alignItems: "center" }}
                >
                  <AiFillDislike size={24} color="lightcoral" />
                  <span style={{ marginLeft: "5px" }}>
                    {character.dislike_count}
                  </span>
                </div>
              </div>
              <div
                className="details-container"
                style={{
                  padding: "15px",
                  backgroundColor: "rgba(0, 0, 0, 0.6)",
                  color: "white",
                  borderBottomLeftRadius: "20px",
                  borderBottomRightRadius: "20px",
                }}
              >
                <h3 style={{ margin: "0 0 5px 0", fontSize: "1.5rem" }}>
                  {character.name}
                </h3>
                <p style={{ margin: "0 0 5px 0", fontSize: "1.1rem" }}>
                  Price: ${character.price.toFixed(2)}
                </p>
                <p style={{ margin: 0, fontSize: "1rem" }}>
                  Colors: {character.colors_available}
                </p>
              </div>
            </div>
          </TinderCard>
        ))}
      </div>
    </div>
  );
}
