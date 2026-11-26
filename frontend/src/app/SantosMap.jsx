import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { config } from "../lib/config";

const santosView = {
  center: [config.map.defaultLng, config.map.defaultLat],
  zoom: config.map.defaultZoom,
  pitch: 60,
  bearing: -22,
};

export default function SantosMap() {
  const container = useRef(null);
  const mapRef = useRef(null);
  const [status, setStatus] = useState("loading");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!config.map.accessToken.startsWith("pk.")) {
      setStatus("token");
      return;
    }
    setStatus("loading");
    let map;
    // O StrictMode pode desmontar a primeira renderização antes do próximo quadro.
    const frame = requestAnimationFrame(() => {
      try {
        map = new mapboxgl.Map({
          container: container.current,
          style: "mapbox://styles/mapbox/standard",
          config: {
            basemap: {
              show3dObjects: true,
              show3dBuildings: true,
              showPointOfInterestLabels: false,
              showTransitLabels: false,
              showLandmarkIcons: false,
              showLandmarkIconLabels: false,
            },
          },
          accessToken: config.map.accessToken,
          ...santosView,
          language: "pt",
          locale: {
            "NavigationControl.ZoomIn": "Aproximar",
            "NavigationControl.ZoomOut": "Afastar",
            "NavigationControl.ResetBearing": "Orientar o mapa para o norte",
          },
        });
        mapRef.current = map;
        map.addControl(
          new mapboxgl.NavigationControl({ visualizePitch: true }),
          "top-left"
        );
        map.on("error", (event) => {
          if (!map.isStyleLoaded() || [401, 403].includes(event.error?.status)) {
            setStatus("error");
          }
        });
        map.once("load", () => setStatus("ready"));
      } catch {
        setStatus("error");
      }
    });
    return () => {
      cancelAnimationFrame(frame);
      mapRef.current = null;
      map?.remove();
    };
  }, [attempt]);

  return (
    <section className="atlas-cartography" aria-label="Mapa interativo de Santos">
      <div className="atlas-canvas" ref={container} />
      {status === "ready" && (
        <button
          className="atlas-reset-view"
          type="button"
          onClick={() => mapRef.current?.easeTo(santosView)}
        >
          Restaurar vista 3D
        </button>
      )}
      {status !== "ready" && (
        <div className="atlas-map-message" role="status">
          {status === "loading" && "Carregando o mapa de Santos…"}
          {status === "token" && "Configure o token público do Mapbox para abrir o mapa."}
          {status === "error" && (
            <>
              Não foi possível carregar o mapa.{" "}
              <button onClick={() => setAttempt((n) => n + 1)}>Tentar novamente</button>
            </>
          )}
        </div>
      )}
    </section>
  );
}
