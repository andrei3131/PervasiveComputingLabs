/**
 * \file
 *         Naive Flooding
 * \author
 *         AESE Group
 */

#include "contiki.h"
#include "net/rime/rime.h"
#include "net/rime/trickle.h"
#include "random.h"
#include "net/netstack.h"

#include "dev/leds.h"
#include "dev/serial-line.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <powertrace.h>

#define NO_OF_NODES 15


struct message{
  uint16_t flood_id;
  uint8_t node_count;
  uint8_t nodes[NO_OF_NODES];
  uint8_t from;
};

struct message payload_send,payload_recv;
static struct trickle_conn trickle;
static struct ctimer message_sent;
//static struct ctimer radio_timer;
/*---------------------------------------------------------------------------*/
PROCESS(main_process, "Trickle Flooding (IMPROVEMENT)");
AUTOSTART_PROCESSES(&main_process);

/* callback function to request a message
 * if node 1 has not seen a message for 10 seconds
 */
static void
request_message(void *ptr){
  ctimer_restart(&message_sent);
  printf("Send me a message\n");
}
//
// static int radio_state = 1;
//
// static void turn_on(void * state_unused) {
//   radio_state = 1;
//   NETSTACK_MAC.on();
// }

/*---------------------------------------------------------------------------*/
static void
trickle_recv(struct trickle_conn *c)
{
  bool received = false;

  packetbuf_copyto(&payload_recv);
  // if(!radio_state) {
  //    radio_state = 0;
  //    NETSTACK_MAC.off(0);
  //    ctimer_set(&radio_timer, CLOCK_SECOND * 7, turn_on, NULL);
  // }

  printf("Broadcast recv from %d of %d with id %d\n", payload_recv.from, payload_recv.nodes[0],payload_recv.flood_id);

  int i = 0;
  for(i = 0; i < payload_recv.node_count;i++){
    if(payload_recv.nodes[i] == linkaddr_node_addr.u8[0]){
	    received = true;
	    break;
    }
  }

  if(payload_recv.node_count > (NO_OF_NODES-1)){
      received = true;
  }

  if(!received){
    payload_recv.nodes[payload_recv.node_count]  = linkaddr_node_addr.u8[0];
    payload_recv.node_count = payload_recv.node_count + 1;
    payload_recv.from = linkaddr_node_addr.u8[0];

    packetbuf_copyfrom(&payload_recv,sizeof(payload_recv));
    trickle_send(&trickle);
    printf("Broadcast message sent\n");

    if(linkaddr_node_addr.u8[0] == 1){
      ctimer_reset(&message_sent);
    }
  }
}

static const struct trickle_callbacks trickle_call = {trickle_recv};

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(main_process, ev, data)
{
  PROCESS_EXITHANDLER(trickle_close(&trickle);)
  char *buf;

  PROCESS_BEGIN();
  powertrace_start(CLOCK_SECOND * 10);
  trickle_open(&trickle, CLOCK_SECOND, 129, &trickle_call);
  if(linkaddr_node_addr.u8[0] == 1){
    ctimer_set(&message_sent, CLOCK_SECOND * 10,request_message,NULL);
  }

  while(1) {
      /* Wait until javascript sends a counter value */
      PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message && data != NULL);
      buf = (char *)data;

      payload_send.flood_id = atoi(buf);
      payload_send.nodes[0] = linkaddr_node_addr.u8[0];
      payload_send.node_count = 1;
      payload_recv.from = linkaddr_node_addr.u8[0];
      packetbuf_copyfrom(&payload_send, sizeof(payload_recv));
      trickle_send(&trickle);
      printf("Broadcast message sent %d\n",atoi(buf));

      if(linkaddr_node_addr.u8[0] == 1){
        ctimer_restart(&message_sent);
      }

    }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
