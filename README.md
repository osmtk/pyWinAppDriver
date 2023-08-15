# Windows Application Driver server in Python
pyWinAppDriver is a service to support Selenium-like UI Test Automation on Windows Applications. 

## Install & Run

## Supported APIs
The following is a list of APIs supported by WinAppDriver:

| Method   | Path  	                                             | pyWinAppDriver |
|----------|-----------------------------------------------------|----------------|
| GET    	 | /status                                           	 |                |
| POST   	 | /session                                          	 |                |
| GET    	 | /sessions                                         	 |                |
| DELETE 	 | /session/:sessionId                               	 |                |
| POST   	 | /session/:sessionId/appium/app/launch             	 |                |
| POST   	 | /session/:sessionId/appium/app/close              	 |                |
| POST   	 | /session/:sessionId/back                          	 |                |
| POST   	 | /session/:sessionId/buttondown                    	 |                |
| POST   	 | /session/:sessionId/buttonup                      	 |                |
| POST   	 | /session/:sessionId/click                         	 |                |
| POST   	 | /session/:sessionId/doubleclick                   	 |                |
| POST   	 | /session/:sessionId/element                       	 |                |
| POST   	 | /session/:sessionId/elements                      	 |                |
| POST   	 | /session/:sessionId/element/active                	 |                |
| GET    	 | /session/:sessionId/element/:id/attribute/:name   	 |                |
| POST   	 | /session/:sessionId/element/:id/clear             	 |                |
| POST   	 | /session/:sessionId/element/:id/click             	 |                |
| GET    	 | /session/:sessionId/element/:id/displayed         	 |                |
| GET    	 | /session/:sessionId/element/:id/element           	 |                |
| GET    	 | /session/:sessionId/element/:id/elements          	 |                |
| GET    	 | /session/:sessionId/element/:id/enabled           	 |                |
| GET    	 | /session/:sessionId/element/:id/equals            	 |                |
| GET    	 | /session/:sessionId/element/:id/location          	 |                |
| GET    	 | /session/:sessionId/element/:id/location_in_view  	 |                |
| GET    	 | /session/:sessionId/element/:id/name              	 |                |
| GET    	 | /session/:sessionId/element/:id/screenshot        	 |                |
| GET    	 | /session/:sessionId/element/:id/selected          	 |                |
| GET    	 | /session/:sessionId/element/:id/size              	 |                |
| GET    	 | /session/:sessionId/element/:id/text              	 |                |
| POST   	 | /session/:sessionId/element/:id/value             	 |                |
| POST   	 | /session/:sessionId/forward                       	 |                |
| POST   	 | /session/:sessionId/keys                          	 |                |
| GET    	 | /session/:sessionId/location                      	 |                |
| POST   	 | /session/:sessionId/moveto                        	 |                |
| GET    	 | /session/:sessionId/orientation                   	 |                |
| GET    	 | /session/:sessionId/screenshot                    	 |                |
| GET    	 | /session/:sessionId/source                        	 |                |
| POST   	 | /session/:sessionId/timeouts                      	 |                |
| GET    	 | /session/:sessionId/title                         	 |                |
| POST   	 | /session/:sessionId/touch/click                   	 |                |
| POST   	 | /session/:sessionId/touch/doubleclick             	 |                |
| POST   	 | /session/:sessionId/touch/down                    	 |                |
| POST   	 | /session/:sessionId/touch/flick                   	 |                |
| POST   	 | /session/:sessionId/touch/longclick               	 |                |
| POST   	 | /session/:sessionId/touch/move                    	 |                |
| POST   	 | /session/:sessionId/touch/scroll                  	 |                |
| POST   	 | /session/:sessionId/touch/up                      	 |                |
| DELETE 	 | /session/:sessionId/window                        	 |                |
| POST   	 | /session/:sessionId/window                        	 |                |
| POST   	 | /session/:sessionId/window/maximize               	 |                |
| POST   	 | /session/:sessionId/window/size                   	 |                |
| GET    	 | /session/:sessionId/window/size                   	 |                |
| POST   	 | /session/:sessionId/window/:windowHandle/size     	 |                |
| GET    	 | /session/:sessionId/window/:windowHandle/size     	 |                |
| POST   	 | /session/:sessionId/window/:windowHandle/position 	 |                |
| GET    	 | /session/:sessionId/window/:windowHandle/position 	 |                |
| POST   	 | /session/:sessionId/window/:windowHandle/maximize 	 |                |
| GET    	 | /session/:sessionId/window_handle                 	 |                |
| GET    	 | /session/:sessionId/window_handles                	 |                |