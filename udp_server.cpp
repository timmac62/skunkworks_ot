#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345
#define BUFFER_SIZE 1024

int main() {
    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t len;
    
    // Create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return -1;
    }
    
    memset(&serverAddr, 0, sizeof(serverAddr));
    memset(&clientAddr, 0, sizeof(clientAddr));
    
    // Fill server information
    serverAddr.sin_family = AF_INET; // IPv4
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");  // Bind to localhost (127.0.0.1)
    serverAddr.sin_port = htons(PORT);  // Bind to port 12345
    
    // Bind the socket with the server address
    if (bind(sockfd, (const struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Bind failed" << std::endl;
        close(sockfd);
        return -1;
    }
    
    std::cout << "UDP server is listening on 127.0.0.1:" << PORT << "..." << std::endl;
    
    len = sizeof(clientAddr);  // Length of client address
    
    while (true) {
        // Clear buffer
        memset(buffer, 0, BUFFER_SIZE);
        
        // Receive message from client
        int n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *) &clientAddr, &len);
        if (n < 0) {
            std::cerr << "Receive failed" << std::endl;
            continue;
        }
        
        // Print received message
        std::cout << "Client: " << buffer << std::endl;
        
        // Optionally send response to client
        const char *message = "Message received";
        sendto(sockfd, message, strlen(message), 0, (const struct sockaddr *) &clientAddr, len);
    }
    
    // Close the socket (unreachable in this example since the server runs indefinitely)
    close(sockfd);
    
    return 0;
}
