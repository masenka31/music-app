                    function likeMe(num) {
                        var nmb = num
                        if (document.getElementById(`heartIcon_${nmb}`).className == 'far fa-heart fa-3x disabled') {
                            document.getElementById(`heartIcon_${nmb}`).className = 'fas fa-heart fa-3x checked'
                            document.getElementById(`banIcon_${nmb}`).className = 'fas fa-ban fa-3x disabled'
                            document.getElementById(`heartValue_${nmb}`).value = `true`
                        }
                        else {
                            document.getElementById(`heartIcon_${nmb}`).className = 'far fa-heart fa-3x disabled'
                            document.getElementById(`banIcon_${nmb}`).className = 'fas fa-ban fa-3x disabled'
                            document.getElementById(`heartValue_${nmb}`).value = `false`
                        }
                    }

                    function banMe(num) {
                        var nmb = num
                        if (document.getElementById(`banIcon_${nmb}`).className == 'fas fa-ban fa-3x disabled') {
                            document.getElementById(`heartIcon_${nmb}`).className = 'far fa-heart fa-3x disabled'
                            document.getElementById(`banIcon_${nmb}`).className = 'fas fa-ban fa-3x ban'
                            document.getElementById(`heartValue_${nmb}`).value = `banned`
                        }
                        else {
                            document.getElementById(`heartIcon_${nmb}`).className = 'far fa-heart fa-3x disabled'
                            document.getElementById(`banIcon_${nmb}`).className = 'fas fa-ban fa-3x disabled'
                            document.getElementById(`heartValue_${nmb}`).value = `false`
                        }
                    }