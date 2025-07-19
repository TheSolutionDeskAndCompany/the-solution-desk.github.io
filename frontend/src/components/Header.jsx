import React from 'react';
import {
  Box,
  Flex,
  HStack,
  Link,
  Button,
  Image,
  Text,
  IconButton,
  useDisclosure,
  useColorModeValue,
  VStack,
  Collapse,
} from '@chakra-ui/react';
import { HamburgerIcon, CloseIcon } from '@chakra-ui/icons';
import Logo from '../assets/logo.svg';

export default function Header() {
  const { isOpen, onToggle, onClose } = useDisclosure();
  const bgColor = useColorModeValue('white', 'darkBg.100');
  const borderColor = useColorModeValue('gray.200', 'neonBlue.500');

  return (
    <Box
      as="nav"
      bg={bgColor}
      borderBottom="2px"
      borderColor={borderColor}
      boxShadow="0 4px 12px rgba(14, 165, 233, 0.15)"
      position="sticky"
      top={0}
      zIndex={1000}
    >
      <Flex
        maxW="7xl"
        mx="auto"
        px={4}
        py={3}
        align="center"
        justify="space-between"
      >
        {/* Logo */}
        <Link href="/" onClick={onClose}>
          <Image src={Logo} alt="The Solution Desk" h="50px" w="auto" />
        </Link>

        {/* Desktop Navigation */}
        <HStack spacing={8} display={{ base: 'none', md: 'flex' }}>
          <HStack spacing={6}>
            <Link
              href="#projects"
              color="neonPink.300"
              fontWeight="bold"
              textTransform="uppercase"
              letterSpacing="0.1em"
              _hover={{
                color: 'neonPink.400',
                textShadow: '0 0 10px rgba(241, 70, 255, 0.5)',
                transform: 'translateY(-1px)',
              }}
              transition="all 0.3s ease"
            >
              💡 Projects
            </Link>
            <Link
              href="#tools"
              color="neonBlue.300"
              fontWeight="bold"
              textTransform="uppercase"
              letterSpacing="0.1em"
              _hover={{
                color: 'neonBlue.400',
                textShadow: '0 0 10px rgba(14, 165, 233, 0.5)',
                transform: 'translateY(-1px)',
              }}
              transition="all 0.3s ease"
            >
              🔧 Tools
            </Link>
            <Link
              href="#kanban"
              color="neonGreen.300"
              fontWeight="bold"
              textTransform="uppercase"
              letterSpacing="0.1em"
              _hover={{
                color: 'neonGreen.400',
                textShadow: '0 0 10px rgba(34, 197, 94, 0.5)',
                transform: 'translateY(-1px)',
              }}
              transition="all 0.3s ease"
            >
              📋 Kanban
            </Link>
            <Link
              href="#account"
              color="neonPurple.300"
              fontWeight="bold"
              textTransform="uppercase"
              letterSpacing="0.1em"
              _hover={{
                color: 'neonPurple.400',
                textShadow: '0 0 10px rgba(168, 85, 247, 0.5)',
                transform: 'translateY(-1px)',
              }}
              transition="all 0.3s ease"
            >
              👤 Account
            </Link>
          </HStack>

          <HStack spacing={4}>
            <Button variant="ghost" size="sm">
              Login
            </Button>
            <Button variant="solid" size="sm">
              Get Started
            </Button>
          </HStack>
        </HStack>

        {/* Mobile Menu Button */}
        <IconButton
          display={{ base: 'flex', md: 'none' }}
          onClick={onToggle}
          icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
          variant="ghost"
          aria-label="Toggle Navigation"
          color="neonPink.300"
          _hover={{
            bg: 'neonPink.900',
            color: 'neonPink.200',
          }}
        />
      </Flex>

      {/* Mobile Navigation */}
      <Collapse in={isOpen} animateOpacity>
        <Box
          pb={4}
          display={{ md: 'none' }}
          bg={bgColor}
          borderTop="1px"
          borderColor={borderColor}
        >
          <VStack spacing={4} align="stretch" px={4}>
            <Link
              href="#projects"
              onClick={onClose}
              color="neonPink.300"
              fontWeight="bold"
              py={2}
              _hover={{ color: 'neonPink.400' }}
            >
              💡 Projects
            </Link>
            <Link
              href="#tools"
              onClick={onClose}
              color="neonBlue.300"
              fontWeight="bold"
              py={2}
              _hover={{ color: 'neonBlue.400' }}
            >
              🔧 Tools
            </Link>
            <Link
              href="#kanban"
              onClick={onClose}
              color="neonGreen.300"
              fontWeight="bold"
              py={2}
              _hover={{ color: 'neonGreen.400' }}
            >
              📋 Kanban
            </Link>
            <Link
              href="#account"
              onClick={onClose}
              color="neonPurple.300"
              fontWeight="bold"
              py={2}
              _hover={{ color: 'neonPurple.400' }}
            >
              👤 Account
            </Link>

            <VStack spacing={3} align="stretch" pt={4}>
              <Button variant="ghost" onClick={onClose} size="sm">
                Login
              </Button>
              <Button variant="solid" onClick={onClose} size="sm">
                Get Started
              </Button>
            </VStack>
          </VStack>
        </Box>
      </Collapse>
    </Box>
  );
}
