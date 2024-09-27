# TheSocialScore

flowchart TD
    %% Certificate Creation Process
    A[Administrator Input Student and Certificate Details] --> B[Generate Digital Certificate (PDF)]
    
    %% Hash Generation
    B --> C[Generate Hash using SHA-256 Algorithm]
    
    %% Blockchain Interaction
    C --> D[Invoke Chaincode for Storing Hash on Hyperledger Fabric]
    
    D --> E{Does Chaincode Exist?}
    E -->|Yes| F[Chaincode Executes Transaction]
    E -->|No| G[Deploy Chaincode (Smart Contract) on Hyperledger Fabric]

    %% Store Hash on Blockchain
    F --> H[Store Certificate Hash, Certificate ID, and Timestamp on Blockchain]
    G --> H

    %% Final Step
    H --> I[Transaction Committed to Ledger]

    %% Blockchain Ledger Interaction
    I --> J[Hash Immutably Stored on Hyperledger Fabric Ledger]

    %% Acknowledge Completion
    J --> K[Certificate Hash Stored Successfully]
