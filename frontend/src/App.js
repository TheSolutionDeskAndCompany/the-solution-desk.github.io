import React from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  Card,
  CardBody,
  SimpleGrid,
  useColorModeValue,
} from '@chakra-ui/react';
import Header from './components/Header';
import './App.css';

function App() {
  const bgColor = useColorModeValue('gray.50', 'darkBg.100');
  const cardBg = useColorModeValue('white', 'darkBg.200');

  return (
    <Box minH="100vh" bg={bgColor}>
      <Header />
      
      {/* Hero Section */}
      <Container maxW="7xl" py={20}>
        <VStack spacing={8} textAlign="center">
          <Heading
            as="h1"
            size="2xl"
            bgGradient="linear(to-r, neonPink.400, neonBlue.400, neonGreen.400)"
            bgClip="text"
            textShadow="0 0 20px rgba(241, 70, 255, 0.3)"
          >
            Welcome to The Solution Desk
          </Heading>
          
          <Text
            fontSize="xl"
            color="neonBlue.200"
            maxW="2xl"
            lineHeight="tall"
          >
            Your cyber-punk powered workspace for managing projects, tools, and workflows 
            with cutting-edge technology and neon-bright efficiency.
          </Text>
          
          <HStack spacing={4}>
            <Button size="lg" variant="solid">
              Get Started
            </Button>
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </HStack>
        </VStack>
      </Container>
      
      {/* Features Section */}
      <Container maxW="7xl" py={16}>
        <VStack spacing={12}>
          <Heading
            as="h2"
            size="xl"
            textAlign="center"
            color="neonPink.300"
            textShadow="0 0 15px rgba(241, 70, 255, 0.4)"
          >
            Cyber-Punk Features
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={8}>
            <Card bg={cardBg} borderColor="neonPink.600" borderWidth="1px">
              <CardBody>
                <VStack spacing={4}>
                  <Text fontSize="3xl">💡</Text>
                  <Heading size="md" color="neonPink.300">
                    Smart Projects
                  </Heading>
                  <Text color="neonBlue.200" textAlign="center">
                    AI-powered project management with neon-bright insights
                  </Text>
                </VStack>
              </CardBody>
            </Card>
            
            <Card bg={cardBg} borderColor="neonBlue.600" borderWidth="1px">
              <CardBody>
                <VStack spacing={4}>
                  <Text fontSize="3xl">🔧</Text>
                  <Heading size="md" color="neonBlue.300">
                    Cyber Tools
                  </Heading>
                  <Text color="neonBlue.200" textAlign="center">
                    Advanced toolset for the digital workspace of tomorrow
                  </Text>
                </VStack>
              </CardBody>
            </Card>
            
            <Card bg={cardBg} borderColor="neonGreen.600" borderWidth="1px">
              <CardBody>
                <VStack spacing={4}>
                  <Text fontSize="3xl">📋</Text>
                  <Heading size="md" color="neonGreen.300">
                    Neon Kanban
                  </Heading>
                  <Text color="neonBlue.200" textAlign="center">
                    Visualize workflows with glowing efficiency metrics
                  </Text>
                </VStack>
              </CardBody>
            </Card>
            
            <Card bg={cardBg} borderColor="neonPurple.600" borderWidth="1px">
              <CardBody>
                <VStack spacing={4}>
                  <Text fontSize="3xl">⚡</Text>
                  <Heading size="md" color="neonPurple.300">
                    Lightning Fast
                  </Heading>
                  <Text color="neonBlue.200" textAlign="center">
                    Blazing performance with cyber-punk aesthetics
                  </Text>
                </VStack>
              </CardBody>
            </Card>
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
}

export default App;
