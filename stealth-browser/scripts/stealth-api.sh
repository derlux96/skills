#!/bin/bash
# Stealth Browser API Wrapper
# Usage: stealth-api.sh <action> [params...]

API_URL="http://localhost:8081"

case "$1" in
    health)
        curl -s "$API_URL/health"
        ;;
    goto)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"action\": \"goto\", \"url\": \"$2\"}"
        ;;
    text|get_text)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d '{"action": "get_text"}'
        ;;
    elements)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d '{"action": "get_interactive_elements"}'
        ;;
    click)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"action\": \"system_click\", \"x\": $2, \"y\": $3}"
        ;;
    type)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"action\": \"system_type\", \"text\": \"$2\"}"
        ;;
    wait)
        curl -s -X POST "$API_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"action\": \"wait_for_element\", \"selector\": \"$2\", \"timeout\": ${3:-10}}"
        ;;
    screenshot)
        curl -s "$API_URL/screenshot/browser?whLargest=512" -o "${2:-screenshot.png}"
        echo "Saved to ${2:-screenshot.png}"
        ;;
    status)
        docker ps --filter "name=stealth-browser" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;
    start)
        docker run -d \
            --name stealth-browser \
            -p 127.0.0.1:8081:8080 \
            -p 127.0.0.1:5901:5900 \
            --read-only \
            --tmpfs /tmp:rw,noexec,nosuid,size=512m \
            --security-opt=no-new-privileges \
            --cap-drop=ALL \
            -v ~/.openclaw/stealth-browser-profile:/userdata \
            -e TZ=Europe/Berlin \
            psyb0t/stealthy-auto-browse:latest
        echo "Container started. Wait 30-60s for initialization."
        ;;
    stop)
        docker stop stealth-browser 2>/dev/null
        docker rm stealth-browser 2>/dev/null
        echo "Container stopped and removed."
        ;;
    restart)
        docker restart stealth-browser 2>/dev/null || echo "Container not running"
        ;;
    *)
        echo "Stealth Browser API Wrapper"
        echo ""
        echo "Usage: $0 <action> [params]"
        echo ""
        echo "Actions:"
        echo "  health              Check API health"
        echo "  goto <url>          Navigate to URL"
        echo "  text                Get page text"
        echo "  elements            List interactive elements"
        echo "  click <x> <y>       OS-level click at coordinates"
        echo "  type <text>         OS-level type text"
        echo "  wait <selector> [timeout]  Wait for element"
        echo "  screenshot [file]   Take screenshot"
        echo "  status              Show container status"
        echo "  start               Start container"
        echo "  stop                Stop and remove container"
        echo "  restart             Restart container"
        ;;
esac
