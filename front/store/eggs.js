export const state = () => ({
  currentAppFromSeller: null,
  currentAppFromBuyer: null,
  currentCalculate: null,
  currentConfCalculate: null,
  currentDeal: null
})

export const mutations = {
  currentAppFromSeller(state, payload) {
    state.currentAppFromSeller = payload
  },
  currentAppFromBuyer(state, payload) {
    state.currentAppFromBuyer = payload
  },
  currentCalculate(state, payload) {
    state.currentCalculate = payload
  },
  currentConfCalculate(state, payload) {
    state.currentConfCalculate = payload
  },
  currentDeal(state, payload) {
    state.currentDeal = payload
  }
}

export const actions = {
  setCurrentTask(context, payload){
    context.commit('currentTask', payload)
  },

  setCurrentAppFromSeller(context, payload) {
    context.commit('currentAppFromSeller', payload)
  },

  setCurrentAppFromBuyer(context, payload) {
    context.commit('currentAppFromBuyer', payload)
  },

  setCurrentCalculate(context, payload) {
    context.commit('currentCalculate', payload)
  },

  setCurrentConfCalculate(context, payload) {
    context.commit('currentConfCalculate', payload)
  },

  setCurrentDeal(context, payload) {
    context.commit('currentDeal', payload)
  },
  
  async postSellerApp(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/application_from_seller/', payload, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Заявка от продавца создана')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        // console.log('isinstance', e.response?.data instanceof Array)
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async getSellerApp(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/application_from_seller/${id}/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },
  
  async patchSellerApp(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/application_from_seller/${payload[1]}/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Заявка от продавца изменена')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },
  
  async postBuyerApp(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/application_from_buyer/', payload, {headers: {Authorization: `Bearer ${token}`}})
      alert('Заявка от покупателя создана')
      if (!data) throw new Error('No response')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async getBuyerApp(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/application_from_buyer/${id}/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },
  
  async patchBuyerApp(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/application_from_buyer/${payload[1]}/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Заявка от покупателя изменена')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async toggleIsActive(context, task) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post(`/eggs/field_is_active_off/`, task, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      switch(task.model_title) {
        case "Заявка от продавца":
          return alert(`${task.model_title} удалена`)
        case "Заявка от покупателя":
          return alert(`${task.model_title} удалена`)
        case "Сделка":
          return alert(`${task.model_title} удалена`)
        case "Просчет":
          return  alert(`${task.model_title} удален`)
        case "Подтвержденный просчет":
          return alert(`${task.model_title} удален`)
      }
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async getModel(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/base_deal/${id}/get_model/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return data[0]
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },
  
  async postCalc(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post(`/eggs/base_deal/0/create_calculate/`, payload, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Просчет создан')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async patchCalc(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${payload[1]}/patch_calculate/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Просчет изменен')
      return data[0]
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async postConfCalc(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${payload[1]}/create_confirmed_calculate/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Подтвержденный просчет создан')
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async patchConfCalc(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${payload[1]}/patch_confirmed_calculate/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Подтвержденный просчет изменен')
      return data[0]
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async patchConfCalcReadyStatus(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${id}/patch_confirmed_calculate/`, {calc_ready: true}, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return alert('Отправлен на подтверждение')
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async addExpense(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/additional_expense/${payload[1]}/update_expense/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return alert('Дополнительный расход добавлен')
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async postDeal(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${payload[0]}/create_deal/`, payload[1], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Сделка создана')
      return 
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async patchDeal(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${payload[1]}/patch_deal/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Сделка изменена')
      return data[0]
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async patchDealStatus(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/base_deal/${id}/patch_deal/`, {deal_status_ready_to_change: true}, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      alert('Статус сделки изменен')
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async getDealDocs(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/documents/${id}/get_deal_docs/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      return data[0]
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  },

  async dealUpload(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/documents/${payload[0]}/patch_deal_docs/`, payload[1], {headers: {Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data'}})
      if (!data) throw new Error('No response')
      alert('Документ загружен')
      return true
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
      else if (e.response?.status === 400) {
        if (!e.response.data[0]) {
          let message = ''
          for (let error of Object.keys(e.response.data)) {
            message += `${error}: ${e.response.data[error][0]} \n`
          }
          alert(message)
        }
        else {
          alert(e.response.data)
        }
      }
    }
  }
}
