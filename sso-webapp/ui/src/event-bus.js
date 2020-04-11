import Vue from 'vue'

/**
 * Event fired once a user logged into the application.
 */
const LOGIN_EVENT = 'LOGIN_EVENT'

/**
 * Event fired once a user logged into the application.
 */
const LOGOUT_EVENT = 'LOGOUT_EVENT'

/**
 * Create an event bus and make it available.
 *
 * An event bus is technically just a vue instance which we use to "emit" events to and listen to them.
 */
const EventBus = new Vue()

/**
 * Fire an event that a user logged in.
 */
export var fireLoginEvent = () => {
  console.log('fireLoginEvent')
  EventBus.$emit(LOGIN_EVENT)
}

/**
 * Register a function to be executed when the user logged in event is fired.
 * @param {Function} callback
 */
export var registerLoginEventListener = (callback) => {
  console.log('registerLoginEventListener')
  EventBus.$on(LOGIN_EVENT, callback)
}

/**
 * Fire an event that a user logged out.
 */
export var fireLogoutEvent = () => {
  console.log('fireLogoutEvent')
  EventBus.$emit(LOGOUT_EVENT)
}

/**
 * Register a function to be executed when the user logged out event is fired.
 *
 * @param {Function} callback
 */
export var registerLogoutEventListener = (callback) => {
  console.log('registerLogoutEventListener')
  EventBus.$on(LOGOUT_EVENT, callback)
}
