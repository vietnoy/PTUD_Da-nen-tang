import React from 'react';
import { TouchableOpacity } from 'react-native';
import { NavigationContainer, } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { Ionicons } from '@expo/vector-icons';

import LoginScreen from './Screens/LoginScreen';
import RegisterScreen from './Screens/RegisterScreen';
import HomeScreen from './Screens/HomeScreen';
import VerifyEmailScreen from './Screens/VerifyEmailScreen';

const Stack = createNativeStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
          <Stack.Screen
            name="Login"
            component={LoginScreen}
            options={{ title: '' ,
                headerShown: false
            }}
          />
          <Stack.Screen
            name="Register"
            component={RegisterScreen}
            options={{ title: '',
               headerShown: false
             }}
          />
          <Stack.Screen
            name="VerifyEmail"
            component={VerifyEmailScreen}
            options={{ title: '',
               headerShown: false
             }}
          />
          <Stack.Screen
            name="Home"
            component={HomeScreen}
            options={({ navigation }) => ({
              title: 'Đi chợ tiện lợi',
              headerLeft: () => (
                <TouchableOpacity onPress={() => navigation.navigate("Setting")
                }>
                  <Ionicons name="person-circle" size={40} color="green" />
                </TouchableOpacity>
              ),
              headerStyle: { backgroundColor: 'lightskyblue' },
              //headerShown: false,
              headerBackVisible: false,
              //headerLeft: () => {return null;}
            })}
          />
          {/* <Stack.Screen name="Setting" component={SettingScreen} /> */}
        </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;