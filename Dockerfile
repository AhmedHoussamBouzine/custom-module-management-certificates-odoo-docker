From odoo:16
# Copy the Times New Roman font file (times-new-roman.ttf) into the container
COPY times-new-roman.ttf /usr/share/fonts/truetype/


# Update the font cache
RUN fc-cache -f -v

# Expose Odoo services
EXPOSE 8069 

USER odoo

CMD ["odoo"]





