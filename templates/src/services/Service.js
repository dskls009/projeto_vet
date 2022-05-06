import { SessionStorage, Notify } from 'quasar'

export function headers () {
    return { 'Authorization': SessionStorage.getItem('token') }
}