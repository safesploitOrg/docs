# Larger Production Architecture (HA)

## Summary

| Colour    | Layer                   | Function                                                                  |
| --------- | ----------------------- | ------------------------------------------------------------------------- |
| 🟣 Purple | 🌐 **Anycast**          | Distributes users between geographic regions / PoPs                       |
| 🔵 Blue   | 🛣️ **BGP**             | Advertises and provides reachability to the service IP                    |
| 🔵 Blue   | 🔀 **ECMP**             | Distributes flows across equivalent network paths / L4 nodes              |
| 🟠 Orange | ⚖️ **L4 Load Balancer** | TCP/UDP connection distribution                                           |
| 🟢 Green  | 🔀 **L7 Load Balancer** | HTTP/HTTPS routing, TLS termination, and host/path/header-based decisions |
| ⚫ Slate   | 🖥️ **Server HA**       | Multiple application instances provide service resilience                 |



## Mermaid

- 🟣 Global / Anycast
- 🔵 Routing / ECMP
- 🟠 L4 load balancing
- 🟢 L7 load balancing
- ⚫ Application servers — slate/grey
- 🇬🇧 / 🇩🇪 Regions

---

```mermaid

flowchart TB

    %% ============================================================
    %% COLOUR DEFINITIONS
    %% ============================================================

    classDef global fill:#7E57C2,stroke:#4527A0,stroke-width:2px,color:#FFFFFF
    classDef router fill:#42A5F5,stroke:#1565C0,stroke-width:2px,color:#FFFFFF
    classDef l4 fill:#FFB74D,stroke:#EF6C00,stroke-width:2px,color:#111111
    classDef l7 fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#FFFFFF
    classDef app fill:#78909C,stroke:#37474F,stroke-width:2px,color:#FFFFFF


    %% ============================================================
    %% CLIENT / GLOBAL LAYER
    %% ============================================================

    USER["🌍 Internet Users"]

    ANYCAST["🌐 Anycast Service IP<br/>203.0.113.10<br/>BGP Advertisement"]

    USER --> ANYCAST

    class ANYCAST global


    %% ============================================================
    %% FRANKFURT REGION
    %% ============================================================

    subgraph FRA["🇩🇪 Frankfurt Region"]

        direction TB

        FRA_ROUTER["🛣️ Edge Router Pair<br/>BGP + ECMP"]


        %% -------------------------
        %% L4 LOAD BALANCING
        %% -------------------------

        FRA_L4_01["⚖️ L4-LB01<br/>TCP / UDP"]
        FRA_L4_02["⚖️ L4-LB02<br/>TCP / UDP"]


        %% -------------------------
        %% L7 LOAD BALANCING
        %% -------------------------

        FRA_L7_01["🔀 L7-LB01<br/>HTTP / HTTPS"]
        FRA_L7_02["🔀 L7-LB02<br/>HTTP / HTTPS"]


        %% -------------------------
        %% APPLICATION SERVERS
        %% -------------------------

        FRA_WEB01["🖥️ Web01"]
        FRA_WEB02["🖥️ Web02"]
        FRA_WEB03["🖥️ Web03"]


        %% -------------------------
        %% ROUTER -> L4
        %% -------------------------

        FRA_ROUTER -->|"ECMP"| FRA_L4_01
        FRA_ROUTER -->|"ECMP"| FRA_L4_02


        %% -------------------------
        %% L4 -> L7
        %% -------------------------

        FRA_L4_01 --> FRA_L7_01
        FRA_L4_01 --> FRA_L7_02

        FRA_L4_02 --> FRA_L7_01
        FRA_L4_02 --> FRA_L7_02


        %% -------------------------
        %% L7 -> APPLICATION
        %% -------------------------

        FRA_L7_01 --> FRA_WEB01
        FRA_L7_01 --> FRA_WEB02
        FRA_L7_01 --> FRA_WEB03

        FRA_L7_02 --> FRA_WEB01
        FRA_L7_02 --> FRA_WEB02
        FRA_L7_02 --> FRA_WEB03

    end


    %% ============================================================
    %% LONDON REGION
    %% ============================================================

    subgraph LONDON["🇬🇧 London Region"]

        direction TB

        LON_ROUTER["🛣️ Edge Router Pair<br/>BGP + ECMP"]


        %% -------------------------
        %% L4 LOAD BALANCING
        %% -------------------------

        LON_L4_01["⚖️ L4-LB01<br/>TCP / UDP"]
        LON_L4_02["⚖️ L4-LB02<br/>TCP / UDP"]


        %% -------------------------
        %% L7 LOAD BALANCING
        %% -------------------------

        LON_L7_01["🔀 L7-LB01<br/>HTTP / HTTPS"]
        LON_L7_02["🔀 L7-LB02<br/>HTTP / HTTPS"]


        %% -------------------------
        %% APPLICATION SERVERS
        %% -------------------------

        LON_WEB01["🖥️ Web01"]
        LON_WEB02["🖥️ Web02"]
        LON_WEB03["🖥️ Web03"]


        %% -------------------------
        %% ROUTER -> L4
        %% -------------------------

        LON_ROUTER -->|"ECMP"| LON_L4_01
        LON_ROUTER -->|"ECMP"| LON_L4_02


        %% -------------------------
        %% L4 -> L7
        %% -------------------------

        LON_L4_01 --> LON_L7_01
        LON_L4_01 --> LON_L7_02

        LON_L4_02 --> LON_L7_01
        LON_L4_02 --> LON_L7_02


        %% -------------------------
        %% L7 -> APPLICATION
        %% -------------------------

        LON_L7_01 --> LON_WEB01
        LON_L7_01 --> LON_WEB02
        LON_L7_01 --> LON_WEB03

        LON_L7_02 --> LON_WEB01
        LON_L7_02 --> LON_WEB02
        LON_L7_02 --> LON_WEB03

    end


    %% ============================================================
    %% GLOBAL ANYCAST ROUTING
    %% ============================================================

    ANYCAST -->|"BGP selects region"| FRA_ROUTER

    ANYCAST -->|"BGP selects region"| LON_ROUTER


    %% ============================================================
    %% APPLY NODE COLOURS
    %% ============================================================

    class FRA_ROUTER,LON_ROUTER router

    class FRA_L4_01,FRA_L4_02,LON_L4_01,LON_L4_02 l4

    class FRA_L7_01,FRA_L7_02,LON_L7_01,LON_L7_02 l7

    class FRA_WEB01,FRA_WEB02,FRA_WEB03,LON_WEB01,LON_WEB02,LON_WEB03 app


    %% ============================================================
    %% REGION STYLING
    %% ============================================================

    style FRA fill:#FFF7E6,stroke:#F57C00,stroke-width:3px

    style LONDON fill:#EAF3FB,stroke:#1565C0,stroke-width:3px
    
```