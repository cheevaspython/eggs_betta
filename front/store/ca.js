export const state = () => ({
  sellers: [],
  buyers: [],
  logists: [],
  buyersDebt: [],
  sellersDebt: [],
  allUsers: [],
  buyerFromMessage: null,
  traderData: null
})

export const mutations = {
  setSellers(state, data) {
    data.forEach(item => {
      switch(item.pay_type) {
        case 1:
          item.pay_type = 'С НДС'
          break
        case 2:
          item.pay_type = 'Без НДС'
          break
        case 3:
          item.pay_type = 'Наличка'
          break
      }
    })
    state.sellers = data
  },

  setBuyers(state, data) {
    data.forEach(item => {
      switch(item.pay_type) {
        case 1:
          item.pay_type = 'С НДС'
          break
        case 2:
          item.pay_type = 'Без НДС'
          break
        case 3:
          item.pay_type = 'Наличка'
          break
      }
    })
    state.buyers = data
  },

  setBuyersDebt(state, data) {
    // data.beznal.forEach(item => {
    //   switch(item.pay_type) {
    //     case 1:
    //       item.pay_type = 'С НДС'
    //       break
    //     case 2:
    //       item.pay_type = 'Без НДС'
    //       break
    //     case 3:
    //       item.pay_type = 'Наличка'
    //       break
    //   }
    // })
    // data.cash.forEach(item => {
    //   switch(item.pay_type) {
    //     case 1:
    //       item.pay_type = 'С НДС'
    //       break
    //     case 2:
    //       item.pay_type = 'Без НДС'
    //       break
    //     case 3:
    //       item.pay_type = 'Наличка'
    //       break
    //   }
    // })
    state.buyersDebt = data
  },

  setSellersDebt(state, data) {
    state.sellersDebt = data
  },

  setLogists(state, data) {
    data.forEach(item => {
      switch(item.pay_type) {
        case 1:
          item.pay_type = 'С НДС'
          break
        case 2:
          item.pay_type = 'Без НДС'
          break
        case 3:
          item.pay_type = 'Наличка'
          break
      }
    })
    state.logists = data
  },
  setUsers(state, data) {
    state.allUsers = data
  },
  setBuyerFromMessage(state, data) {
    state.buyerFromMessage = data
  },
  setTraderData(state, data) {
    state.traderData = data
  }
}

export const actions = {
  setTraderData(context, payload){
    context.commit('setTraderData', payload)
  },

  async getSellers(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/seller_card/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      context.commit('setSellers', data)
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

  async postSeller(context, seller) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/seller_card/', seller, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      alert('Продавец создан')
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

  async getBuyers(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/buyer_card/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      context.commit('setBuyers', data)
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

  async postBuyer(context, buyer) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/buyer_card/', buyer, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      alert('Покупатель создан')
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
      return false
    }
  },

  async getBuyerFromMessage(context, inn) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/limit_duty_eggs/${inn}/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      const buyer = data[0]
      buyer.status = "Покупатель"
      buyer.debt_deals = data[1]
      context.commit('setBuyerFromMessage', buyer)
      return buyer
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

  async getCurrentLogic(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/logic_card/${id}/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
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

  async getLogists(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/logic_card/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      context.commit('setLogists', data)
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

  async postLogic(context, logic) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/logic_card/', logic, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      alert('Логист создан')
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

  async getBuyersDebt(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/balance/0/list_buyer/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      context.commit('setBuyersDebt', data)
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

  async getSellersDebt(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/balance/0/list_seller/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      context.commit('setSellersDebt', data)
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

  async entryPayment(context, encroachment) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch('/eggs/limit_duty_eggs/', encroachment, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      alert('Платеж внесен')
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

  async getAllUsers(context) {
    const token = localStorage.getItem('access_token')
    try {
      const data = await this.$axios.get('/users/users_list/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      context.commit('setUsers', data.data)
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

  async buyerCashDocs(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const data = await this.$axios.patch(`/eggs/documents_buyer_cash/${payload[1]}/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
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

  async documentsContract(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const data = await this.$axios.patch(`/eggs/documents/${payload[1]}/patch_docs_contract/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
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

  async getTails(context, id) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get(`/eggs/tails/${id}/get_tail/`, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
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

  async payTails(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.patch(`/eggs/tails/${payload[1]}/pay_tails/`, payload[0], {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
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
}
